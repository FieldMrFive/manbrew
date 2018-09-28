import os
import shutil

__all__ = ["link",
           "unlink",
           "remove",
           "list_func",
           "root"]


def link(*args, **kwargs):
    app_args, manager, logger, manbrew_root = (
        kwargs['app_args'], kwargs['manager'], kwargs['logger'], kwargs['manbrew_root'])

    src_path = os.path.join(manbrew_root, "containers", app_args.Container)
    if not os.path.exists(src_path):
        logger.warning("container %s not exists.", app_args.Container)
        return
    manager.link(container=app_args.Container,
                 src_path=src_path,
                 dst_path=app_args.dst)


def unlink(*args, **kwargs):
    app_args, manager = kwargs['app_args'], kwargs['manager']
    manager.unlink(container=app_args.Container)


def remove(*args, **kwargs):
    app_args, manager, logger, manbrew_root = (
        kwargs['app_args'], kwargs['manager'], kwargs['logger'], kwargs['manbrew_root'])
    if manager.container_linked(app_args.Container):
        manager.unlink(container=app_args.Container)

    rm_dir = os.path.join(manbrew_root, "containers", app_args.Container)
    if os.path.exists(rm_dir):
        logger.info("remove dir: %s", rm_dir)
        shutil.rmtree(rm_dir)
    else:
        logger.warning("%s not exists.", rm_dir)


def list_func(*args, **kwargs):
    manager, logger, manbrew_root = kwargs['manager'], kwargs['logger'], kwargs['manbrew_root']
    container_dir = os.path.join(manbrew_root, "containers")
    message = "List all containers\n"
    containers = []
    for container in os.listdir(container_dir):
        if not os.path.isdir(os.path.join(container_dir, container)):
            continue
        message += "%s" + (": linked\n" if manager.container_linked(container) else ": not linked\n")
        containers.append(container)
    logger.info(message, *containers)


def root(*args, **kwargs):
    manbrew_root = kwargs['manbrew_root']
    print(manbrew_root)
