#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	camlp-streams
Summary:	Stream and Genlex libraries for OCaml
Name:		ocaml-%{module}
Version:	5.0.1
Release:	1
License:	LGPL
Group:		Libraries
Source0:	https://github.com/ocaml/camlp-streams/archive/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	afc874b25f7a1f13e8f5cfc1182b51a7
URL:		https://github.com/ocaml/camlp-streams
BuildRequires:	ocaml >= 1:4.00
BuildRequires:	ocaml-dune
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}
%if %{without ocaml_opt}
%define		no_install_post_strip	1
# no opt means no native binary, stripping bytecode breaks such programs
%define		_enable_debug_packages	0
%endif

%description
This package contains files needed to run bytecode executables using
TEMPLATE library.

%description -l pl.UTF-8
Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających biblioteki TEMPLATE.

%package devel
Summary:	TEMPLATE binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania TEMPLATE dla OCamla - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq ocaml

%description devel
This package contains files needed to develop OCaml programs using
TEMPLATE library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów w OCamlu
używających biblioteki TEMPLATE.

%prep
%setup -q -n %{module}-%{version}

%build
dune build --verbose

%install
rm -rf $RPM_BUILD_ROOT

dune install --destdir=$RPM_BUILD_ROOT

# cleanup after dune install
# sources
 %{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/%{module}/*.ml
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc/%{module}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE README.md
%dir %{_libdir}/ocaml/%{module}
%{_libdir}/ocaml/%{module}/META
%{_libdir}/ocaml/%{module}/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/%{module}/*.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/%{module}/*.cmi
%{_libdir}/ocaml/%{module}/*.cmt
%{_libdir}/ocaml/%{module}/*.cmti
%{_libdir}/ocaml/%{module}/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/%{module}/*.o
%{_libdir}/ocaml/%{module}/*.cmx
%{_libdir}/ocaml/%{module}/*.cmxa
%endif
%{_libdir}/ocaml/%{module}/dune-package
%{_libdir}/ocaml/%{module}/opam
