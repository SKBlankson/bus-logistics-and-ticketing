import 'package:ashesi_bus/widgets/text.dart';
import 'package:flutter/material.dart';

class FormButton extends StatelessWidget{


  FormButton({
    super.key, 
    required this.text,
    required this.onPressed,
    this.textColor = Colors.white,
    this.buttonColor = const Color(0xFF011936),
    this.width = 0.4
  });

  String text;
  Function() onPressed;
  Color textColor;
  Color buttonColor;
  double width;

  @override
  Widget build (BuildContext context){

    return Container(
      margin: const EdgeInsets.only(top: 6, bottom: 6),
      width: MediaQuery.of(context).size.width * width,
      child: ElevatedButton(
        onPressed: onPressed,
        style: ElevatedButton.styleFrom(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(10),
          ),
          elevation: 0,
          backgroundColor: buttonColor,
        ),
        child: HeaderText(
          text: text,
          color: textColor,
        ),
      )
    );
  }


}