import 'package:ashesi_bus/pages/bottom_navigation.dart';
// import 'package:ashesi_bus/pages/home.dart';
import 'package:ashesi_bus/widgets/button.dart';
import 'package:ashesi_bus/widgets/form.dart';
import 'package:ashesi_bus/widgets/text.dart';
import 'package:flutter/material.dart';
import 'sign_up.dart';

class Login extends StatefulWidget {

  Login({
    super.key
  });

  LoginState createState() => LoginState();


}

class LoginState extends State<Login> {

  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwdController = TextEditingController();

  @override
  Widget build (BuildContext context) {

    return MaterialApp (

      home: Scaffold(

        appBar: AppBar(
          title: const Text(
            "Login"
          ),
          elevation: 0,
          backgroundColor: Color(0xFF923D41)
        ),

        body: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [

            AppFormField(
              controller: emailController, 
              labelledText: "Email Address"
            ),

            AppFormField(
              controller: passwdController, 
              labelledText: "Password"
            ),

            FormButton(
              text: "Login", 
              onPressed: () {
                Navigator.push(
                  context, 
                  MaterialPageRoute(builder: (context) => BottomNavigation())
                );
              }
            ),

            HyperText(
              text: CenteredText(
                text: MainText(
                  text: "Don't have an account? Sign Up",
                  color: Colors.black,
                )
              ),
              onTap: () {
                Navigator.push(
                  context, 
                  MaterialPageRoute(builder: (context) => SignUp())
                );
              }
            )



          ],
          
        )
      )
    );


  }



}