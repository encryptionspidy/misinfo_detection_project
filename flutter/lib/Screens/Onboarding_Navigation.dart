import 'package:falo/Onboarding.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:smooth_page_indicator/smooth_page_indicator.dart';

import '../utility/dart_utility.dart';

class Onboarding_Navigation extends StatelessWidget {



  @override
  Widget build(BuildContext context) {
    final controller=OnboardingController.instance;
    final dark= Utility.isDarkMode(context);
    return Positioned(
        bottom: Utility.bottomNavigationdefaultHeight,
        left: 30,
        child:
        SmoothPageIndicator(
          controller: controller.pageController,
          onDotClicked: controller.dotNavigationCLick,
          count: 3,
          effect: ExpandingDotsEffect(activeDotColor: dark? Colors.white:Colors.blue,dotHeight: 6),
        ));
  }
}