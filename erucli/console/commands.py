# coding: utf-8

from erucli.console.app import (
    register_app_version,
    set_app_env,
    delete_app_env,
    list_app_env_content,
    list_app_containers,
    list_app_versions,
    list_app_env_names,
    deploy_private_container,
    deploy_public_container,
    build_image,
    build_log,
    remove_containers,
    offline_version,
    container_log,
    bind_container_network,
    bind_container_eip,
    release_container_eip,
)
from erucli.console.entity import (
    create_pod,
    create_network,
    create_host,
    host_bind_eip,
    host_release_eip,
    host_get_eip,
)


commands = {
    'app:register': register_app_version,
    'app:setenv': set_app_env,
    'app:getenv': list_app_env_content,
    'app:delenv': delete_app_env,
    'app:listenv': list_app_env_names,
    'app:dpri': deploy_private_container,
    'app:dpub': deploy_public_container,
    'app:build': build_image,
    'app:listcontainer': list_app_containers,
    'app:listversion': list_app_versions,
    'app:rmcontainer': remove_containers,
    'app:offline': offline_version,

    'pod:create':create_pod,
    'host:create': create_host,
    'host:bind-eip': host_bind_eip,
    'host:release-eip': host_release_eip,
    'host:get-eip': host_get_eip,

    'log:task': build_log,
    'log:container': container_log,

    'net:create': create_network,
    'net:bind': bind_container_network,
    'net:bind-eip': bind_container_eip,
    'net:release-eip': release_container_eip,
}
