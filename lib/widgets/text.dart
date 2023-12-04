import 'package:flutter/material.dart';

/// This class represents the text widget being used throughout the app
class MainText extends StatelessWidget {

  MainText ({
    super.key,
    required this.text,
    this.fontSize,
    this.color = Colors.black,
    this.fontWeight = FontWeight.w300
  });

  final String text;
  double? fontSize;
  Color color;
  FontWeight fontWeight;

  @override
  Widget build (BuildContext context) {

    return Text(
      text,
      style: TextStyle(
        fontSize: fontSize,
        fontWeight: fontWeight,
        fontFamily: 'Arial',
        color: color
      )
    );

  }

}


/// This widget represents header text that would be used in the app
class HeaderText extends StatelessWidget {

  HeaderText({
    super.key,
    required this.text,
    this.color = Colors.white
  });

  String text;
  Color color;

  @override
  Widget build (BuildContext context) {
    return MainText(
      text: text,
      fontSize: 15,
      fontWeight: FontWeight.w600,
      color: color,
    );
  }

}


class LeftAlignedText extends StatelessWidget {

  LeftAlignedText({
    super.key,
    required this.text,
    this.color = Colors.white
  });

  Widget text;
  Color color;

  @override
  Widget build (BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(left: 10, right: 10),
      child: Align(
        alignment: Alignment.centerLeft,
        child: text
      )
    );
  }

}


/// This widet represents sub-header text that would be used in the app
class SubHeaderText extends StatelessWidget {

  SubHeaderText({
    super.key,
    required this.text,
    this.color = Colors.white
  });

  String text;
  Color color;

  @override
  Widget build (BuildContext context) {
    return MainText(
      text: text,
      fontSize: 14,
      fontWeight: FontWeight.w500,
      color: color,
    );
  }

}

/// This widet represents text that is used for further information that would be used in the app
class SubText extends StatelessWidget {

  SubText({
    super.key,
    required this.text,
    this.color = Colors.white,
    this.fontSize = 10
  });

  String text;
  Color color;
  double fontSize;


  @override
  Widget build (BuildContext context) {
    return MainText(
      text: text,
      fontSize: fontSize,
      fontWeight: FontWeight.w300,
      color: color,
    );
  }

}


/// This widget represents centered text that would be used in the app
class CenteredText extends StatelessWidget {

  CenteredText({
    super.key,
    required this.text
  });

  Widget text;

  @override
  Widget build (BuildContext context) {
    return Center(
      child: text
    );
  }

}

class HyperText extends StatelessWidget {

  HyperText({
    super.key,
    required this.text,
    required this.onTap
  });

  Widget text;
  Function() onTap;

  @override
  Widget build (BuildContext context) {

    return GestureDetector(
      onTap: onTap,
      child: text
    );

  }

}
