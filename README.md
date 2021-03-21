Marvell/Aquantia AQC111u MultiGigabit 2.5GbE/5GbE USB3 NIC Driver for XCP-ng :rocket:
=====================================================================================

[![build](https://github.com/itnok/xcp-ng-aqc111u-driver/actions/workflows/main.yml/badge.svg?branch=master&event=push)](https://github.com/itnok/xcp-ng-aqc111u-driver/actions/workflows/main.yml) ![Release](https://img.shields.io/github/v/release/itnok/xcp-ng-aqc111u-driver)

This repository allows to create RPM packages for all versions of XCP-ng supported by [xcp-ng-build-env](https://github.com/xcp-ng/xcp-ng-build-env). The AQC111u driver source is automatically downloaded from the [Sabrent website as distributed for their NT-SS5G](https://www.sabrent.com/download/nt-ss5g/) and automatically configured, built and packed in a containerized environment for each desired version of XCP-ng.

---

## :hammer: How to build

In order to build the RPM package a machine running Linux and providing Docker is necessary. To create the package follow the steps below:

```bash
# mkdir -p aqc111u-driver-build
# cd aqc111u-driver-build
# git clone https://github.com/xcp-ng/xcp-ng-build-env.git
# git clone https://github.com/itnok/xcp-ng-aqc111u-driver.git
# ls xcp-ng-build-env/Dockerfile* | \
      xargs -I %%%% sed -i \
      's~RUN *useradd builder~RUN groupadd -g '"$(id -g)"' builder \&\& useradd -u '"$(id -u)"' -g '"$(id -g)"' builder~g' \
      %%%%
# ./xcp-ng-build-env/run.py -b <X.Y> --build-local xcp-ng-aqc111u-driver/ --rm

```

The value `<X.Y>` should be replaced with the version of XCP-ng the driver is planned to be used for _(e.g. 7.5, 8.0, 8.2, etc.)_. At the end of the build process a RPM package will be avaialble inside the `xcp-ng-aqc111u-driver/RPMS/x86_64/` directory.


## :test_tube: How to use

After the installation of the RPM package to the target XCP-ng host, it should suffice to plug the USB3 NIC in and the dedicated `aqc111.ko` kernel module should be automatically loaded. Nevertheless it would be probably still necessary to manually add the new PIF to XCP-ng. Because of the autoconfiguration of the USB adapter the name of the network adapter might change after each reboot or if plugged back in after disconnecting it. To avoid this behavior and prevent XCP-ng to leave uunused PIFs around it is recommended to add a new `udev` rule based on the MAC address of the NIC.

```bash
# echo 'SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="<aa:bb:cc:dd:ee:ff>", ATTR{type}=="1", KERNEL=="eth*", NAME="eth<X>"' \
    > /etc/udev/rules.d/70-persistent-net.rules

```

The value `<aa:bb:cc:dd:ee:ff>` should be replaced with the real MAC address of the NIC. The value `<X>` with an integer to idientify the PIF. Without this operation being performed the PIF will assume names like `side-1234-eth0`, `side-5432-eth1` and the like. Then the new PIF _(now with a consistent name across restarts and pluggin/unplugging)_ can be _"introduced"_ to XCP-ng:

```bash
# xe pif-introduce host-uuid=<xcp-ng-host-uuid> device=eth<X> mac=<aa:bb:cc:dd:ee:ff>

```

The value `<xcp-ng-host-uuid>` can be simply retrieved with the command `xe host-list`. the values for both `<aa:bb:cc:dd:ee:ff>` and `<X>` should be identical to the ones used in the previous step creating the `udev` rule.

_(For more details about the CLI commands to [manage physical NICs, please refer to the official XCP-ng documentation](https://xcp-ng.org/docs/networking.html#manage-physical-nics))_

