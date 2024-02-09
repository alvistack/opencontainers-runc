# Copyright 2024 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

Name: cri-o-runc
Epoch: 100
Version: 1.1.10
Release: 1%{?dist}
Summary: Tool for spawning and running OCI containers
License: Apache-2.0
URL: https://github.com/opencontainers/runc/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: glibc-static
BuildRequires: golang-1.22
BuildRequires: libseccomp-devel
BuildRequires: pkgconfig
BuildRequires: protobuf-devel
Provides: oci-runtime

%description
runc is a CLI tool for spawning and running containers according to the
OCI specification. It is designed to be as minimal as possible, and is
the workhorse of Docker. It was originally designed to be a replacement
for LXC within Docker, and has grown to become a separate project
entirely. This package is a fork of the "runc' package, specifically for
cri-o.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
mkdir -p sbin
set -ex && \
    export CGO_ENABLED=1 && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w" \
        -tags 'seccomp' \
        -o ./sbin/runc .

%install
install -Dpm755 -d %{buildroot}%{_prefix}/lib/cri-o-runc/sbin
install -Dpm755 -t %{buildroot}%{_prefix}/lib/cri-o-runc/sbin/ sbin/runc

%files
%license LICENSE
%dir %{_prefix}/lib/cri-o-runc
%dir %{_prefix}/lib/cri-o-runc/sbin/
%{_prefix}/lib/cri-o-runc/sbin/*

%changelog
