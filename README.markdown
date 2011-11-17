# ZenPacks.zenoss.CloudFoundry
Please watch the [Monitoring Cloud Foundry][] video for a quick introduction that covers most of the details below.

## About
This project is a [Zenoss][] extension (ZenPack) that makes it possible to monitor the capacity and performance of applications running on a [Cloud Foundry][] platform. This works for applications hosted in a local micro-cloud or a hosted environment such as the one offered by [VMware][] at cloudfoundry.com.

[Cloud Foundry][] is an open PAAS (Platform as a Service) project initiated by [VMware][].

## Installation
You must first have, or install, Zenoss 3.1.0 or later. Core and Enterprise versions are supported. You can download the free Core version of Zenoss from <http://community.zenoss.org/community/download>.

### Normal Installation (packaged egg)
Depending on what version of Zenoss you're running you will need a different
package. Download the appropriate package for your Zenoss version from the list
below.

 * Zenoss 4.1: [Latest Package for Python 2.7][]
 * Zenoss 3.0 - 4.0: [Latest Package for Python 2.6][]

Then copy it to your Zenoss server and run the following commands as the zenoss
user.

    zenpack --install <package.egg>
    zenoss restart

### Developer Installation (link mode)
If you wish to further develop and possibly contribute back to the CloudFoundry ZenPack you should clone the [git repository][], then install the ZenPack in developer mode using the following commands.

    git clone git://github.com/zenoss/ZenPacks.zenoss.CloudFoundry.git
    zenpack --link --install ZenPacks.zenoss.CloudFoundry
    zenoss restart

## Usage
Once the CloudFoundry ZenPack is installed you can add endpoints by going to the infrastructure screen and clicking the normal button for adding devices. You will find a new option labeled, "Add CloudFoundry Endpoint."

Choose that option and you'll be presented with a dialog asking for the following inputs.

 1. Target - An example would be api.cloudfoundry.com or api.vcap.me.
 2. Email - The email address you used to register.
 3. Password

Once you click Add Zenoss will contact the target and get all of the operationally interesting information that exists. Once it is complete you'll find a new device in the /CloudFoundy device class with the same name as the target you entered into the dialog. Click into this new device to see everything that was discovered.

The following elements are discovered:

 * Frameworks
  * Runtimes
  * App Servers
 * System Services
 * Provisioned Services
 * Apps
  * App Instances

The following performance metrics are collected:

 * Per-Endpoint (target)
  * Limits
   * App URIs
   * Apps
   * Memory
   * Services
  * Usage
   * App URIs
   * Apps
   * App Instances
   * Running App Instances
   * Memory
   * Services
  * Utilization
   * App URIs
   * Apps
   * Memory
   * Services
 * Per-App
  * Resources
   * Memory
   * Disk
  * Usage
   * CPU (average across instances)
   * Memory
   * Disk
  * Utilization
   * Memory
   * Disk
  * Instances
   * Total
   * Running
  * Services
  * URIs
 * Per-App Instance
  * Quota
   * Memory
   * Disk
  * Usage
   * CPU
   * Memory
   * Disk
  * Utilization
   * Memory
   * Disk

The following default thresholds are configured:

 * Over 99% utilization of..
  * Endpoint App URIs
  * Endpoint Apps
  * Endpoint Memory
  * Endpoint Services
  * App CPU (average across instances)
  * App Memory
  * App Disk
  * App Instance CPU
  * App Instance Memory
  * App Instance Disk
 * Less than 1 running instance per App


[Monitoring Cloud Foundry]: <http://www.youtube.com/watch?v=uDUUVTWXCPE>
[Zenoss]: <http://www.zenoss.com/>
[Latest Package for Python 2.7]: <https://github.com/downloads/zenoss/ZenPacks.zenoss.CloudFoundry/ZenPacks.zenoss.CloudFoundry-1.0.2-py2.7.egg>
[Latest Package for Python 2.6]: <https://github.com/downloads/zenoss/ZenPacks.zenoss.CloudFoundry/ZenPacks.zenoss.CloudFoundry-1.0.2-py2.6.egg>
[git repository]: <https://github.com/zenoss/ZenPacks.zenoss.CloudFoundry>
[VMware]: <http://www.vmware.com/>
[Cloud Foundry]: <http://cloudfoundry.com/>
