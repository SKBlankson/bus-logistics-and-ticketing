import 'package:ashesi_bus/widgets/text.dart';
import 'package:flutter/material.dart';

class TripDetailsContainer extends StatelessWidget {
  final String tripID;
  final String fromLocation;
  final String toLocation;
  final String stops;
  final String tripTime;

  TripDetailsContainer({
    required this.tripID,
    required this.fromLocation,
    required this.toLocation,
    this.stops = "0",
    required this.tripTime,
  });


  @override
  Widget build(BuildContext context) {

    return Container(
      color: Colors.white,
      margin: const EdgeInsets.only(left: 15, right: 15),
      width: MediaQuery.of(context).size.width,

      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          // first container
          Container(
            padding: EdgeInsets.all(20),
            decoration: const BoxDecoration(
              borderRadius: BorderRadius.only(
                topLeft: Radius.circular(20.0),
                bottomLeft: Radius.circular(20.0),
              ),
              color: Color(0xFF011936),
            ),
            child: HeaderText(
              text: tripID,
            ),
          ),

          // second container
          Container(
            padding: EdgeInsets.all(10),
            child: MainText(
              text: "$fromLocation to $toLocation",
              color: Color(0xFF909090),
            ),
          ),

          // third container
          Container(
            padding: const EdgeInsets.all(20),
            decoration: const BoxDecoration(
              borderRadius: BorderRadius.only(
                topRight: Radius.circular(20.0),
                bottomRight: Radius.circular(20.0),
              ),
              color: Color(0xFF923D41),
            ),
            child: HeaderText(
              text: tripTime,
            ),
          ),
        ],
      ),
    );
  }
}
