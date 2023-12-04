import 'package:flutter/material.dart';

class History extends StatefulWidget {

  History({
    super.key,
  });

 
  HistoryState createState() => HistoryState();
}

class HistoryState extends State<History>{

   @override
  Widget build(BuildContext context){
    return Scaffold(
      appBar: AppBar(
        title: Text("Ashesi Bus"),
        backgroundColor: Color(0xFF923D41),
        elevation: 0
      ),
    
    );

  }
}