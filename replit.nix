{pkgs}: {
  deps = [
    pkgs.lsof
    pkgs.glibcLocales
    pkgs.openssl
    pkgs.postgresql
  ];
}
