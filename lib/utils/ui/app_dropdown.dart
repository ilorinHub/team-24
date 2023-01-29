import 'package:flutter/material.dart';

class AppDropdown extends StatefulWidget {
  AppDropdown(
      {this.items = const ['item 1', 'item 2', 'item 3'],
      this.value,
      this.onChanged,
      super.key});

  List<String> items;
  String? value;
  Function(String)? onChanged;

  @override
  State<AppDropdown> createState() => _AppDropdownState();
}

class _AppDropdownState extends State<AppDropdown> {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(5),
        border: Border.all(color: Colors.grey),
      ),
      child: DropdownButton(
        underline: const SizedBox(),
        isExpanded: true,
        icon: const Icon(Icons.keyboard_arrow_down_rounded),
        items: widget.items
            .map((e) => DropdownMenuItem(value: e, child: Text(e)))
            .toList(),
        value: widget.value ?? widget.items.first,
        onChanged: (value) {
          setState(() => widget.value = value);
          if (widget.onChanged != null) widget.onChanged!(value!);
        },
      ),
    );
  }
}
