import os
import json
from core import TextStyle

__all__ = ['LinkManager']


class LinkManager(object):
    def __init__(self, record_file, logger):
        self.record_file = record_file
        self.logger = logger
        if not os.path.exists(record_file):
            self.record = {}
        else:
            with open(self.record_file, 'r') as f:
                self.record = json.load(f)
        self.new_record = []

    def __del__(self):
        with open(self.record_file, 'w') as f:
            json.dump(self.record, f)

    def resolve_all_link(self, src_path, dst_path):
        if os.path.isfile(src_path) or os.path.islink(dst_path):
            raise RuntimeError('%s exists. Clean dir or brew unlink first.' % dst_path)

        for target in os.listdir(src_path):
            if not os.path.exists(os.path.join(dst_path, target)):
                self.make_link(os.path.join(src_path, target),
                               os.path.join(dst_path, target))
                self.new_record.append(os.path.join(dst_path, target))
            else:
                self.resolve_all_link(os.path.join(src_path, target),
                                      os.path.join(dst_path, target))

    def link(self, container, src_path, dst_path):
        if self.container_linked(container):
            self.logger.warning('%s already linked.', TextStyle.bold(container))
            return

        self.new_record = []

        self.logger.info('link %s', TextStyle.bold(container))
        try:
            self.resolve_all_link(src_path, dst_path)
            opt_link = os.path.join(dst_path, 'opt', container)
            if os.path.exists(opt_link):
                raise RuntimeError('%s exists. Clean dir or brew unlink first.' % opt_link)
            self.make_link(src_path, opt_link)
            self.new_record.append(opt_link)
        except RuntimeError as e:
            self.remove_link(self.new_record)
            raise e
        self.logger.info('%s linked.', TextStyle.bold(container))
        self.record[container] = self.new_record

    def unlink(self, container):
        if not self.container_linked(container):
            self.logger.warning('%s not linked.', TextStyle.bold(container))
            return

        self.logger.info('unlink %s', TextStyle.bold(container))
        self.remove_link(self.record[container])
        self.logger.info('%s unlinked.', TextStyle.bold(container))
        del self.record[container]

    def remove_link(self, links):
        for link in links:
            self.logger.info('unlink %s', link)
            os.remove(link)

    def make_link(self, src, dst):
        os.symlink(src, dst)
        self.logger.info('link %s -> %s', dst, src)

    def container_linked(self, container):
        if self.record is None:
            return False
        return container in self.record
