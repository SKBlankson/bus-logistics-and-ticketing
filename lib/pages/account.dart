import 'package:ashesi_bus/widgets/button.dart';
import 'package:ashesi_bus/widgets/form.dart';
import 'package:flutter/material.dart';

class Account extends StatefulWidget {
  Account({
    super.key,
  });

  @override
  AccountState createState() => AccountState();
}

class AccountState extends State<Account> {
  final TextEditingController nameController = TextEditingController();
  final TextEditingController emailController = TextEditingController();
  final TextEditingController momoController = TextEditingController();
  // final TextEditingController passwdController = TextEditingController();

  // void _saveAccount() {
  //   // Get the values from the text controllers
  //   String name = nameController.text;
  //   String email = emailController.text;
  //   String momo = momoController.text;

  //   // TODO: Implement save logic here
  //   // You can use the values to save the account details

  //   // Clear the text controllers after saving
  //   nameController.clear();
  //   emailController.clear();
  //   momoController.clear();
  // }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Ashesi Bus"),
        backgroundColor: const Color(0xFF923D41),
        elevation: 0,
      ),
      body: Container(
        padding: const EdgeInsets.all(10),
        child: ListView(
          children: [
            SizedBox(height: 20),

            Icon(
              Icons.account_circle, 
              size: 100, 
              color: Colors.grey
            ),

            AppFormField(
              controller: nameController,
              labelledText: "Name",
              enabled: false,
            ),

            SizedBox(height: 20),

            AppFormField(
              controller: emailController,
              labelledText: "Email Address",
              enabled: false,
            ),

            SizedBox(height: 20),

            AppFormField(
              controller: momoController, 
              labelledText: "Mobile Money Number",
            ),

            SizedBox(height: 20),

            // FormButton(
            //   text: "Save", 
            //   onPressed: _saveAccount
            // ),

            SizedBox(height: 20),

            // TODO: Implement logout logic here
          ],
        ),
      ),
    );
  }
  }
              
