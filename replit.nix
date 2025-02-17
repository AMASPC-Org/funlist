{ pkgs }: {
  deps = [
    pkgs.lsof
    pkgs.glibcLocales
    pkgs.openssl
    pkgs.postgresql
    pkgs.python310
    pkgs.net-tools
  ];
}
            