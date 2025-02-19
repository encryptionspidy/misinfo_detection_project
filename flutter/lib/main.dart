import 'package:falo/LoginScreen.dart';
import 'package:falo/Onboarding.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:get/get_core/src/get_main.dart';
import 'Screens/Onboarding_Navigation.dart';
import 'Screens/Onboarding_circular.dart';
import 'Screens/Onboarding_skp.dart';
import 'TIMAGES.dart';
import 'Screens/Onboarding_Page.dart';
import 'chatScreen/MainChat.dart';
void main() => runApp(OnboardingScreen());

class OnboardingScreen extends StatelessWidget {
  const OnboardingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: ActiveScreen(),
      initialRoute: "/",
      routes: {
        "/Login":(context)=>Loginscreen(),
        "/chat":(context)=>ChatApp()
      },
    );
  }
}

class ActiveScreen extends StatefulWidget {
  const ActiveScreen({super.key});

  @override
  State<ActiveScreen> createState() => _ActiveScreenState();

}

class _ActiveScreenState extends State<ActiveScreen>  {
final controllor=Get.put(OnboardingController());
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          PageView(
            controller: controllor.pageController,
            onPageChanged: controllor.updatePageIndicator,
            children: [
              Onboarding_Page (image: Timages.slide_1logo, title: Timages.title, subtitle: Timages.subtitle),
              Onboarding_Page (image: Timages.slide_2logo, title: Timages.title1, subtitle: Timages.subtitle1),
              Onboarding_Page (image: Timages.slide_3logo, title: Timages.title2, subtitle: Timages.subtitle2),

            ],
          ),
          Onboarding_skip(),
          Onboarding_Navigation(),
          Onboarding_CirculorBotton()
        ],
      ),
    );
    ;
  }
}






