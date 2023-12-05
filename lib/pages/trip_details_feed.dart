import 'package:flutter/material.dart';

import '../widgets/container.dart';

class Trip{
  final String fromLocation;
  final String toLocation;
  final String stops;
  final String tripTime;

  Trip({
    required this.fromLocation,
    required this.toLocation,
    required this.stops,
    required this.tripTime
  });
}

List<Trip> trips = [
    Trip(
      // tripID: '1',
      fromLocation: 'Ashesi',
      toLocation: 'Accra',
      stops: 'Stop1, Stop2',
      tripTime: "7:00pm",
    ),
    Trip(
      // tripID: '2',
      fromLocation: 'Accra',
      toLocation: 'Kumasi',
      stops: 'Stop3, Stop4',
      tripTime: "8:00pm",
    ),
    Trip(
      // tripID: '3',
      fromLocation: 'Ashesi',
      toLocation: 'Takoradi',
      stops: 'Stop5, Stop6',
      tripTime: "9:00pm",
    ),
    // Add more trips as needed
  ];

class TripDetailsFeed extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      shrinkWrap: true,
      itemCount: trips.length,
      itemBuilder: (context, index) {
        Trip trip = trips[index];

        return Column(
          children: [
            TripDetailsContainer(
              tripID: index.toString(),
              fromLocation: trip.fromLocation,
              toLocation: trip.toLocation,
              stops: trip.stops,
              tripTime: trip.tripTime,
            ),
            const SizedBox(height: 20,),
          ],
        );
      },
    );
  }
}

  
