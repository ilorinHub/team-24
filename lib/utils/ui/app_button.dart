import 'package:flutter/material.dart';
import 'package:kw_irs/constants/app_colors.dart';

class AppButton extends StatefulWidget {
  AppButton(
      {required this.label,
      required this.onTap,
      this.backgrounColor = AppColors.primary,
      this.labelColor = Colors.white,
      super.key});

  Color? backgrounColor;
  Color? labelColor;
  String label;
  Function() onTap;

  @override
  State<AppButton> createState() => _AppButtonState();
}

class _AppButtonState extends State<AppButton> {
  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      height: 50,
      child: MaterialButton(
        onPressed: widget.onTap,
        color: widget.backgrounColor,
        elevation: 1,
        child: Text(
          widget.label,
          style: TextStyle(color: widget.labelColor),
        ),
      ),
    );
  }
}
