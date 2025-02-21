{ pkgs }: {
  deps = [
    pkgs.nano
    pkgs.glibcLocales
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
    pkgs.python311Full
    pkgs.tesseract
    pkgs.imagemagick_light
  ];
}
