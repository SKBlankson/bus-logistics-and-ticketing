import 'package:ashesi_bus/pages/bottom_navigation.dart';
import 'package:ashesi_bus/pages/login.dart';
import 'package:ashesi_bus/widgets/button.dart';
import 'package:ashesi_bus/widgets/form.dart';
import 'package:ashesi_bus/widgets/text.dart';
import 'package:flutter/material.dart';

class SignUp extends StatefulWidget {

  SignUp({
    super.key
  });

  SignUpState createState() => SignUpState();


}

class SignUpState extends State<SignUp> {

  final TextEditingController fnameController = TextEditingController();
  final TextEditingController lnameController = TextEditingController(); 
  final TextEditingController emailController = TextEditingController();
  final TextEditingController telNoController = TextEditingController();
  final TextEditingController momoController = TextEditingController();
  final TextEditingController passwdController = TextEditingController();
  final TextEditingController confirmPasswdController = TextEditingController();


  @override
  Widget build (BuildContext context) {

    return Scaffold (

      appBar: AppBar(
        title: const Text(
          "Sign Up"
        ),
        backgroundColor: Color(0xFF923D41),
        elevation: 0,
      ),

      body: ListView(
        // mainAxisAlignment: MainAxisAlignment.center,
        children: [

          AppFormField(
            controller: fnameController, 
            labelledText: "First Name"
          ),

          AppFormField(
            controller: lnameController, 
            labelledText: "Last name"
          ),

          AppFormField(
            controller: emailController, 
            labelledText: "Email Address"
          ),

          AppFormField(
            controller: telNoController, 
            labelledText: "Telephone Number"
          ),

          AppFormField(
            controller: momoController, 
            labelledText: "Momo (Mobile) Number "
          ),

          AppFormField(
            controller: passwdController, 
            labelledText: "Password"
          ),

          AppFormField(
            controller: confirmPasswdController, 
            labelledText: "Confirm Password"
          ),

          Center(
            child: FormButton(
              text: "Sign Up", 
              onPressed: () {
                Navigator.pushReplacement(
                  context, 
                  MaterialPageRoute(builder: (context) => BottomNavigation())
                );
              }
            )
          ),

          HyperText(
            text: CenteredText(
              text: MainText(
                text: "Already have an account? Login",
                color: Colors.black,
              )
            ),
            onTap: () {
              Navigator.push(
                context, 
                MaterialPageRoute(builder: (context) => Login())
              );
            }
          )
        ],
        
      )
    );

  }



}