import 'package:ashesi_bus/pages/account.dart';
import 'package:ashesi_bus/pages/history.dart';
import 'package:ashesi_bus/pages/home.dart';
import 'package:flutter/material.dart';

class BottomNavigation extends StatefulWidget {
  @override
  _BottomNavigationState createState() => _BottomNavigationState();
}

class _BottomNavigationState extends State<BottomNavigation> {

  int _currentIndex = 0;

  final List<Widget> _pages = [
    Home(),
    History(),
    Account(),
  ];

  @override
  Widget build(BuildContext context) {
    return MaterialApp(

      home: Scaffold(
      
        body: _pages[_currentIndex],
        
        bottomNavigationBar: BottomNavigationBar(
          currentIndex: _currentIndex,
        
          onTap: (int index) {
            setState(() {
              _currentIndex = index;
            });
          },

          items: const [
            BottomNavigationBarItem(
              icon: Icon(Icons.home),
              label: "Home",
            ),

            BottomNavigationBarItem(
              icon: Icon(Icons.access_time),
              label: "History",
            ),

            BottomNavigationBarItem(
              icon: Icon(Icons.person),
              label: "Account",
            ),
          ],
        ),
      )
    );
  }
}