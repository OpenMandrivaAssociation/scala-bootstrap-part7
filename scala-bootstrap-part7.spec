Name:		scala-bootstrap-part7
Version:	1
Release:	1
Summary:	Second half of the seventh Scala 2.10.7 bootstrap checkpoint
Group:		Development/Java
License:	Apache-2.0
URL:		https://github.com/vxtls/scala
Source0:	scala-bootstrap-2.10.7.tar.gz
Patch0:		scala-bootstrap-part7-stop.patch

BuildArch:	noarch
BuildRequires:	scala-bootstrap-part7a = 1
BuildRequires:	java-1.8.0-openjdk-devel
BuildRequires:	clang
BuildRequires:	git-core
BuildRequires:	make
BuildRequires:	python
BuildRequires:	tar
BuildRequires:	patch

%description
Checkpoint of the vxtls Scala bootstrap climb from
v2.10.0-M4+277dc7c through v2.10.0-M4+035224a.
It resumes from the scala-bootstrap-part7a seed.
The seed also keeps the v2.10.0-M4+3393624 pack jars.
v2.10.0-M6+7050335 builds from that stage.
This package does not provide the Scala 2.10.7 compiler.

%prep
%autosetup -n scala-bootstrap-2.10.7 -p1
find . -type f \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -print > binaries.list
if [ -s binaries.list ]; then
	cat binaries.list
	exit 1
fi
test -s LICENSE
test -s compile.sh
test -s scripts/pack-seed.sh
test -s scripts/check-part.sh
test -s scripts/buildit.sh
grep -q resume_skip scripts/buildit.sh
grep -q rebuild_host_natives scripts/buildit.sh
grep -q SCALA_BOOT_UNTIL compile.sh
grep -q SCALA_BOOT_SEED compile.sh
grep -q bcp-flag scripts/pack-seed.sh
grep -q bcp-flag scripts/check-part.sh
grep -q GROUP5 scripts/pack-seed.sh
test "$(grep -c group4_uses_source_fjbg scripts/pack-seed.sh)" = 2

%build
set -eo pipefail
export JAVA_HOME=$(ls -d %{_jvmdir}/java-1.8.0-openjdk-* | head -n 1)
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
export SCALA_BOOT_SEED=%{_datadir}/scala-bootstrap-part7a/seed
export SCALA_BOOT_FROM=v2.10.0-M4+277dc7c-bootstrap
export SCALA_BOOT_UNTIL=v2.10.0-M4+035224a-bootstrap
bash ./compile.sh

%install
set -eo pipefail
mkdir -p %{buildroot}%{_datadir}/scala-bootstrap-part7
cp -a dist/seed %{buildroot}%{_datadir}/scala-bootstrap-part7/
test -s %{buildroot}%{_datadir}/scala-bootstrap-part7/seed/until-stage
grep -qx 'v2.10.0-M4+035224a-bootstrap' %{buildroot}%{_datadir}/scala-bootstrap-part7/seed/until-stage
grep -qx 'v2.10.0-M4+035224a+b51f067-bootstrap' %{buildroot}%{_datadir}/scala-bootstrap-part7/seed/next-stage
grep -qx 'v2.10.0-M4+035224a-bootstrap' %{buildroot}%{_datadir}/scala-bootstrap-part7/seed/pred-stage
grep -qx -- '-javabootclasspath' %{buildroot}%{_datadir}/scala-bootstrap-part7/seed/bcp-flag
grep -qx 1 %{buildroot}%{_datadir}/scala-bootstrap-part7/seed/scala-boot-lib
test -s %{buildroot}%{_datadir}/scala-bootstrap-part7/seed/stages/v2.10.0-M4+035224a-bootstrap/build/pack/lib/scala-compiler.jar
test -s %{buildroot}%{_datadir}/scala-bootstrap-part7/seed/stages/v2.10.0-M4+3393624-bootstrap/build/pack/lib/scala-library.jar
test -s %{buildroot}%{_datadir}/scala-bootstrap-part7/seed/stages/v2.10.0-M4+3393624-bootstrap/build/pack/lib/scala-compiler.jar
test -s %{buildroot}%{_datadir}/scala-bootstrap-part7/seed/stages/v2.10.0-M4+035224a-bootstrap/build/java8-charbuffer-overrides.jar
test -s %{buildroot}%{_datadir}/scala-bootstrap-part7/seed/stages/v2.10.0-M4+035224a-bootstrap/build/java8-legacy-stubs.jar
test -s %{buildroot}%{_datadir}/scala-bootstrap-part7/seed/stages/v2.10.0-M4+035224a-bootstrap/build/java8-filtered-stubs.jar
if [ -e %{buildroot}%{_datadir}/scala-bootstrap-part7/seed/stages/v2.10.0-M4+035224a-bootstrap/build/libs/forkjoin.jar ]; then
	echo forkjoin jar is not a seed of this checkpoint
	exit 1
fi
if [ -e %{buildroot}%{_datadir}/scala-bootstrap-part7/seed/stages/way2scala-2.0-stage10-bootstrap/distribs/unix/scala-2.0-stage10-bootstrap/share/scala/lib/fjbg.jar ]; then
	echo fjbg jar is not a seed of this checkpoint
	exit 1
fi

%check
set -eo pipefail
export JAVA_HOME=$(ls -d %{_jvmdir}/java-1.8.0-openjdk-* | head -n 1)
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
bash ./scripts/check-part.sh %{buildroot}%{_datadir}/scala-bootstrap-part7/seed

%files
%{_datadir}/scala-bootstrap-part7
%license LICENSE
