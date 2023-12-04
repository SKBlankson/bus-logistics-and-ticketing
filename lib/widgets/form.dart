import 'package:ashesi_bus/widgets/text.dart';
import 'package:flutter/material.dart';


class AppFormField extends StatelessWidget{

  AppFormField ({
    super.key,
    required this.controller,
    required this.labelledText,
    this.hintText,
    this.obscureText = false

  });

  TextEditingController controller;
  String labelledText;
  String? hintText;
  bool obscureText;

  @override
  Widget build(BuildContext context){
    return Center(
      child: Container(
        margin:const EdgeInsets.only(top:6, bottom:6),
        width: MediaQuery.of(context).size.width * 0.8,
        child:TextFormField(
          controller: controller,
          decoration: InputDecoration(
            hintText: hintText,
            labelText: labelledText,
            hintStyle: const TextStyle(
              color: Colors.grey
            ),
            labelStyle: const TextStyle (
              color: Colors.black87
            )
          ),
        ),
      ),
    );
      
  }

}


class TripDetailsField extends StatelessWidget{

  TripDetailsField({
    super.key,
    required this.controller
  });

  TextEditingController controller;

  @override
  Widget build(BuildContext context){
    return TextFormField(
      controller: controller
    );
  }
}