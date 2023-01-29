import 'package:flutter/material.dart';

buildAppBar({required BuildContext context, String title = ''}) => AppBar(
      elevation: 0,
      backgroundColor: Colors.transparent,
      title: Text(
        title,
        style: TextStyle(
            color: Theme.of(context).textTheme.bodyText1!.color, fontSize: 14),
      ),
      centerTitle: true,
      leading: BackButton(
        color: Theme.of(context).iconTheme.color,
      ),
    );
