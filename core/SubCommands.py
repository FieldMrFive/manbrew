import os
import shutil
from core import Font

__all__ = ["SubCommands"]


def container_exist(*args, **kwargs):
    app_args, logger, manbrew_root = kwargs['app_args'], kwargs['logger'], kwargs['manbrew_root']
    container_path = os.path.join(manbrew_root, "containers", app_args.container)
    if not os.path.exists(container_path):
        logger.warning("%s not exists.", Font.BOLD(app_args.container))
        return False
    return True


class SubCommands(object):
    @staticmethod
    def link(*args, **kwargs):
        if not container_exist(*args, **kwargs):
            return

        app_args, manager, logger, manbrew_root = (
            kwargs['app_args'], kwargs['manager'], kwargs['logger'], kwargs['manbrew_root'])

        src_path = os.path.join(manbrew_root, "containers", app_args.container)
        manager.link(container=app_args.container,
                     src_path=src_path,
                     dst_path=app_args.dst)

    @staticmethod
    def unlink(*args, **kwargs):
        if not container_exist(*args, **kwargs):
            return

        app_args, manager = kwargs['app_args'], kwargs['manager']
        manager.unlink(container=app_args.container)

    @staticmethod
    def remove(*args, **kwargs):
        if not container_exist(*args, **kwargs):
            return

        app_args, manager, logger, manbrew_root = (
            kwargs['app_args'], kwargs['manager'], kwargs['logger'], kwargs['manbrew_root'])

        if manager.container_linked(app_args.container):
            manager.unlink(container=app_args.container)

        rm_dir = os.path.join(manbrew_root, "containers", app_args.container)
        if os.path.exists(rm_dir):
            logger.info("remove dir: %s", rm_dir)
            shutil.rmtree(rm_dir)
            logger.info("%s removed.", Font.BOLD(app_args.container))

    @staticmethod
    def list(*args, **kwargs):
        manager, logger, manbrew_root = kwargs['manager'], kwargs['logger'], kwargs['manbrew_root']
        container_dir = os.path.join(manbrew_root, "containers")
        message = "List All Containers\n"
        containers = []
        for container in os.listdir(container_dir):
            if not os.path.isdir(os.path.join(container_dir, container)):
                continue
            message += "%s" + (": linked\n" if manager.container_linked(container) else ": not linked\n")
            containers.append(Font.BOLD(container))
        logger.info(message, *containers)

    @staticmethod
    def root(*args, **kwargs):
        manbrew_root = kwargs['manbrew_root']
        print(manbrew_root)
