import 'package:flutter/material.dart';

import '../widgets/container.dart';

class Trip{
  final String fromLocation;
  final String toLocation;
  final String stops;
  final DateTime tripTime;

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
      tripTime: DateTime(2023, 11, 25, 10, 0),
    ),
    Trip(
      // tripID: '2',
      fromLocation: 'Accra',
      toLocation: 'Kumasi',
      stops: 'Stop3, Stop4',
      tripTime: DateTime(2023, 11, 25, 13, 30),
    ),
    Trip(
      // tripID: '3',
      fromLocation: 'Ashesi',
      toLocation: 'Takoradi',
      stops: 'Stop5, Stop6',
      tripTime: DateTime(2023, 11, 25, 15, 0),
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

  
