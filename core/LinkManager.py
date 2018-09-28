import yaml
import os

__all__ = ["LinkManager"]


class LinkManager(object):
    def __init__(self, record_filename, logger):
        self.record_filename = record_filename
        self.logger = logger
        if not os.path.exists(record_filename):
            self.record = {}
        else:
            with open(self.record_filename, "r") as fin:
                self.record = yaml.load(fin)
        self.new_record = []

    def resolve_all_link(self, src_path, dst_path):
        if os.path.isfile(src_path) or os.path.islink(dst_path):
            raise RuntimeError("%s exists. Clean dir or brew unlink first." % dst_path)

        for target in os.listdir(src_path):
            if not os.path.exists(os.path.join(dst_path, target)):
                self.make_link(os.path.join(src_path, target),
                               os.path.join(dst_path, target))
                self.new_record.append(os.path.join(dst_path, target))
            else:
                self.resolve_all_link(os.path.join(src_path, target),
                                      os.path.join(dst_path, target))

    def link(self, container, src_path, dst_path):
        if container in self.record:
            self.logger.warning("container %s already linked.", container)
            return

        self.new_record = []

        try:
            self.resolve_all_link(src_path, dst_path)
            opt_link = os.path.join(dst_path, "opt", container)
            if os.path.exists(opt_link):
                raise RuntimeError("%s exists. Clean dir or brew unlink first." % opt_link)
            self.make_link(src_path, opt_link)
            self.new_record.append(opt_link)
        except RuntimeError:
            self.remove_link(self.new_record)
            raise

        self.record[container] = self.new_record

    def unlink(self, container):
        if container not in self.record:
            self.logger.warning("container %s not linked.", container)
            return
        self.remove_link(self.record[container])
        del self.record[container]

    def __del__(self):
        with open(self.record_filename, "w") as fout:
            self.record = yaml.dump(self.record, fout, default_flow_style=False)

    def remove_link(self, links):
        for link in links:
            self.logger.info("rm %s", link)
            os.remove(link)

    def make_link(self, src, dst):
        os.symlink(src, dst)
        self.logger.info("link %s", dst)