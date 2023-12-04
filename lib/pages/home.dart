import 'package:ashesi_bus/pages/bottom_navigation.dart';
import 'package:ashesi_bus/pages/trip_details_feed.dart';
import 'package:ashesi_bus/widgets/button.dart';
import 'package:ashesi_bus/widgets/text.dart';
// import 'package:ashesi_bus/widgets/container.dart';
import 'package:flutter/material.dart';

class Home extends StatefulWidget{
  
    Home({
      super.key
    });
  
    HomeState createState() => HomeState();
}

class HomeState extends State<Home>{

  @override
  Widget build(BuildContext context){

    return Scaffold(
      appBar: AppBar(
        title: Text("Ashesi Bus"),
        backgroundColor: Color(0xFF923D41),
        elevation: 0
      ),


      body: ListView(

        children: [ 

          // red container
          Container(
            padding: const EdgeInsets.all(10),
            width: MediaQuery.of(context).size.width,
            color: const Color(0xFF923D41),
            child: Column(

              children: [

                // Upcoming Trips
                LeftAlignedText(
                  text: HeaderText(
                    text: "Upcoming Trips",
                  )
                ),

                const SizedBox(height: 20,),

                Row (
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    const Icon(
                      Icons.directions_bus,
                      color: Colors.white,
                      size: 40,
                    ),

                    const SizedBox(width: 10,),

                    HeaderText(text: "5:10pm"),

                    const SizedBox(width: 10,),

                    SubHeaderText(text: "19/30 seats booked"),

                  ], 
                ),

                const SizedBox(height: 20,),

                
                Align(
                  alignment: Alignment.centerLeft,
                  child: Container(
                    
                    width: MediaQuery.of(context).size.width * 0.6,
                    color: Colors.white,
                    child: DropdownButtonFormField(
                      hint: LeftAlignedText(
                        text: SubText(
                          text: "Select a seat",
                          color: Colors.black,
                          fontSize: 14,
                        )
                      ),
                      items: [
                        DropdownMenuItem(
                          value: "Ashesi to Accra",
                          child: MainText(text:"Ashesi to Accra"),
                        ),
                        DropdownMenuItem(
                          value: "Accra to Ashesi",
                          child: MainText(text: "Accra to Ashesi"),
                        )
                      ],
                      onChanged: (value) {}, 
                    )
                  )
                ),

                const SizedBox(height: 10,),

                Align(
                  alignment: Alignment.centerLeft,
                  child: Container(
                    
                    width: MediaQuery.of(context).size.width * 0.6,
                    color: Colors.white,
                    child: DropdownButtonFormField(
                      hint: LeftAlignedText(
                        text: SubText(
                          text: "Select a seat",
                          color: Colors.black,
                          fontSize: 14,
                        )
                      ),
                      items: [
                        DropdownMenuItem(
                          value: "Ashesi to Accra",
                          child: MainText(text:"Ashesi to Accra"),
                        ),
                        DropdownMenuItem(
                          value: "Accra to Ashesi",
                          child: MainText(text: "Accra to Ashesi"),
                        )
                      ],
                      onChanged: (value) {}, 
                    )
                  )
                ),

                Row (
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
            
                    SubText(
                      text: "Ashesi -> Accra",
                      color: Colors.white,
                      fontSize: 14,
                    ),

                    const SizedBox(width: 10,),

                    Align(
                      alignment: Alignment.centerRight,
                      child: FormButton(
                        text: "Pay Now",
                        buttonColor: Colors.white,
                        textColor: Colors.black,
                        onPressed: () {},
                        width: 0.3,
                      )
                    ),

                  ], 
                ),

                
              ],

            ),
          ),

          SizedBox(height: 20,),
          

          // white (future trips) container
          Container(
            
            width: MediaQuery.of(context).size.width,
            child: Column(
              // mainAxisAlignment: MainAxisAlignment.start,
              children: [
                
                LeftAlignedText(
                  text: HeaderText(
                    text: "Future Trips",
                    color: Colors.black,
                  )
                ),

                const SizedBox(height: 20,),

                // upcoming trips feed
                // TripDetailsContainer(
                //   tripID: "1",
                //   fromLocation: "Ashesi",
                //   toLocation: "Kumasi",
                //   stops: "Stop1-Stop2-Stop3",
                //   tripTime: "5:10pm",
                // ),
                TripDetailsFeed(),
                
              ],

            ),

          ),
        ],

      ),

    );

  }

  
}