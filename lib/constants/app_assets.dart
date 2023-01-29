class AppAssets {
  static const svg = _Svg();
  static const image = _Image();
}

class _Image {
  const _Image();
  //
  String get logo => 'assets/images/logo.png';
}

class _Svg {
  const _Svg();
  //
  String get logo => 'assets/svgs/logo.svg';
}
