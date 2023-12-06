{ sources ? import ./npins, pkgs ? import sources.nixpkgs {}, lib ? pkgs.lib }:
let
  inherit (lib) optionalString;
in
rec {
  buildReferenceUBoot = { nand ? false, ax ? false }: (pkgs.buildUBoot {
    src = ./.;
    version = "2018.09";
    defconfig = if nand then "mt7621_nand${lib.optionalString ax "_ax"}_rfb_defconfig" else "mt7621${lib.optionalString ax "_ax"}_rfb_defconfig";
    extraMeta.platforms = [
      "mipsel-linux"
    ];
    filesToInstall = [
      # NAND image (MT7621)
      (if nand then
        "spl/u-boot-mt7621-nand-spl.img"
      else
        "u-boot-mt7621-spl.bin")
        "u-boot-mt7621.bin"
        # Real bootloader
        "u-boot-lzma.img"
    ];
  }).overrideAttrs (old: {
    depsBuildBuild = old.depsBuildBuild ++ [ pkgs.buildPackages.python2 ];
  });

  ubootNor = buildReferenceUBoot { };
  ubootNand = buildReferenceUBoot { nand = true; };
  ubootAxNor = buildReferenceUBoot { ax = true; };
  ubootAxNand = buildReferenceUBoot { nand = true; ax = true; };
}
