import 'package:flutter/material.dart';

class AppTextField extends StatefulWidget {
  AppTextField(
      {this.label,
      this.hint,
      required this.controller,
      this.prefixIcon,
      this.keyboardType = TextInputType.text,
      super.key});

  String? label;
  String? hint;
  IconData? prefixIcon;
  TextEditingController controller;
  TextInputType keyboardType;

  @override
  State<AppTextField> createState() => _AppTextFieldState();
}

class _AppTextFieldState extends State<AppTextField> {
  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: widget.controller,
      keyboardType: widget.keyboardType,
      decoration: InputDecoration(
        border: OutlineInputBorder(
            gapPadding: 15, borderRadius: BorderRadius.circular(5)),
        labelText: widget.label,
        hintText: widget.hint,
        prefixIcon: (widget.prefixIcon != null)
            ? Icon(
                widget.prefixIcon,
              )
            : null,
      ),
    );
  }
}
