#!/bin/bash

curl -d  "ip=10.10.102.17,host_status=online" http://10.10.102.13:8000/webkvm/manager_kvm/
