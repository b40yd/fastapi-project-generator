#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

import re
import time

from app.core.config import logger, settings


class InputError(Exception):
    pass


class InvalidSystemClock(Exception):
    pass


class InvalidUserAgentError(Exception):
    pass


class SnowFlake(object):
    def __init__(self, worker_id=0, data_center_id=0):
        self.worker_id = worker_id
        self.data_center_id = data_center_id

        self.logger = logger

        # stats
        self.ids_generated = 0

        # Tue, 21 Mar 2006 20:50:14.000 GMT
        self.twepoch = settings.twepoch

        self.sequence = 0
        self.worker_id_bits = 5
        self.data_center_id_bits = 5
        self.max_worker_id = -1 ^ (-1 << self.worker_id_bits)
        self.max_data_center_id = -1 ^ (-1 << self.data_center_id_bits)
        self.sequence_bits = 12

        self.worker_id_shift = self.sequence_bits
        self.data_center_id_shift = self.sequence_bits + self.worker_id_bits
        self.timestamp_left_shift = (self.sequence_bits + self.worker_id_bits +
                                     self.data_center_id_bits)
        self.sequence_mask = -1 ^ (-1 << self.sequence_bits)

        self.last_timestamp = -1

        # Sanity check for worker_id
        if self.worker_id > self.max_worker_id or self.worker_id < 0:
            raise InputError(
                "worker_id",
                "worker id can't be greater than %i or less than 0" %
                self.max_worker_id,
            )

        if self.data_center_id > self.max_data_center_id or self.data_center_id < 0:
            raise InputError(
                "data_center_id",
                f"data center id can't be greater than "
                f"{self.max_data_center_id} or less than 0",
            )

        self.logger.info(
            f"worker starting. timestamp left shift {self.timestamp_left_shift}"
            f",data center id bits {self.data_center_id_bits}, worker id bits "
            f"{self.worker_id_bits},"
            f" sequence bits {self.sequence_bits}, worker id {self.worker_id}")

    def _time_gen(self):
        return int(time.time() * 1000)

    def _till_next_millis(self, last_timestamp):
        timestamp = self._time_gen()
        while last_timestamp <= timestamp:
            timestamp = self._time_gen()

        return timestamp

    def _next_id(self):
        timestamp = self._time_gen()

        if self.last_timestamp > timestamp:
            self.logger.warning(
                f"clock is moving backwards. Rejecting request "
                f"until {self.last_timestamp}")
            raise InvalidSystemClock(
                f"Clock moved backwards. Refusing to generate id for "
                f"{self.last_timestamp} milliseocnds")

        if self.last_timestamp == timestamp:
            self.sequence = (self.sequence + 1) & self.sequence_mask
            if self.sequence == 0:
                timestamp = self._till_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = (((timestamp - self.twepoch) << self.timestamp_left_shift)
                  | (self.data_center_id << self.data_center_id_shift)
                  | (self.worker_id << self.worker_id_shift)
                  | self.sequence)
        self.ids_generated += 1
        return new_id

    def get_worker_id(self):
        return self.worker_id

    def get_timestamp(self):
        return self._time_gen()

    def get_id(self):
        new_id = self._next_id()
        self.logger.debug(
            f"id: {new_id} worker_id: "
            f"{self.worker_id}  data_center_id: {self.data_center_id}")
        return new_id

    def get_datacenter_id(self):
        return self.data_center_id
