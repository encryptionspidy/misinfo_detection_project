import 'package:falo/Onboarding.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:iconsax/iconsax.dart';

import '../utility/dart_utility.dart';

class Onboarding_CirculorBotton extends StatelessWidget {
  const Onboarding_CirculorBotton({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Positioned(
      bottom: 38.0,
      right: Utility.defaultSpace,
      child: ElevatedButton(
          onPressed: () =>OnboardingController.instance.nextPage(context),
          style: ElevatedButton.styleFrom(
            shape: CircleBorder(),
            backgroundColor: Colors.blue,
            foregroundColor: Colors.red,
          ),
          child: Icon(Iconsax.arrow_right_3,color: Colors.white,)),
    );
  }
}
