import 'package:flutter/material.dart';

class Account extends StatefulWidget {

  Account({
    super.key,
  });

 
  @override
  AccountState createState() => AccountState();
}

class AccountState extends State<Account>{

   @override
  Widget build(BuildContext context){
    return Scaffold(

      appBar: AppBar(
        title: const Text("Ashesi Bus"),
        backgroundColor: const Color(0xFF923D41),
        elevation: 0
      ),
  
    );

  }
}