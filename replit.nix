{ pkgs }: {
  deps = [
    pkgs.python311Full
    pkgs.imagemagick_light
    pkgs.cacert
    pkgs.zlib
    pkgs.tk
    pkgs.tcl
    pkgs.openjpeg
    pkgs.libxcrypt
    pkgs.libwebp
    pkgs.libtiff
    pkgs.libjpeg
    pkgs.libimagequant
    pkgs.lcms2
    pkgs.freetype
    pkgs.glibcLocales
    pkgs.nano
    pkgs.mailutils
    pkgs.tesseract
  ];
}
