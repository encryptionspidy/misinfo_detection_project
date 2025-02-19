
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import '../Onboarding.dart';
import '../utility/dart_utility.dart';

class Onboarding_skip extends StatelessWidget {
  const Onboarding_skip({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Positioned(
        top: Utility.getAppBarHeight(),
        right: Utility.defaultSpace,
        child: TextButton(
          onPressed: ()=>OnboardingController.instance.skipPage(context),
          style: TextButton.styleFrom(
            backgroundColor: Colors.blue,

          ),
          child: Text("Skip",
            style:TextStyle(
                fontSize: 16,
                color: Colors.white,
                fontFamily: 'Retrofont'
            ),),));
  }
}