import 'dart:convert';
import 'package:ashesi_bus/classes/shared_pref.dart';
import 'package:ashesi_bus/classes/user.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart';

class AuthProvider with ChangeNotifier {


  Future<Map<String, dynamic>> login(String email, String password) async {

    Map<String,dynamic> result;

    final Map<String, dynamic> loginData = 
      {
        'email': email,
        'password': password
      };
  

    Response response = await post(
      Uri.http(""),
      body: json.encode(loginData),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      
      final Map<String, dynamic> responseData = json.decode(response.body);

      Map<String, dynamic> userData = responseData['data'];

      User authUser = User.fromJson(userData);

      UserPreferences().saveUser(authUser);


      result = {'status': true, 'message': 'Successful', 'user': authUser};
    } else {

      result = {
        'status': false,
        'message': json.decode(response.body)['error']
      };
    }
    return result;
  }

}