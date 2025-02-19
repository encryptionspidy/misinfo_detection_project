import 'package:animated_text_kit/animated_text_kit.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class Onboarding_Page extends StatelessWidget {
  final String image,title,subtitle;
  Onboarding_Page ({
    required this.image, required this.title, required this.subtitle,
  });


  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        TweenAnimationBuilder(
          tween: Tween<Offset>(
            begin: Offset(0, 0),
            end: Offset(0, 10),
          ),
          duration: Duration(milliseconds: 1000),
          curve: Curves.elasticOut,  // This adds the bounce effect
          builder: (context, value, child) {
            return Transform.translate(
              offset: value,
              child: child,
            );
          },
          child: Image.asset(
            image,  // Replace with your image path
            width: 400,
            height: 400,
          ),
        ),
        // SizedBox(height: 30.0,),
        AnimatedTextKit(
          animatedTexts: [
            WavyAnimatedText(title,
                textStyle: TextStyle(
                    color: Colors.blue,
                    fontSize: 30,
                    fontWeight: FontWeight.bold,
                    fontFamily: 'Retrofont'
                ))
          ],
          isRepeatingAnimation: true,
          onTap: () {
            print("Tap Event");
          },
        ),
        Padding(padding: EdgeInsets.all(30),
          child: Text(subtitle,
            textAlign: TextAlign.center,
            style: TextStyle(
              fontSize: 12,
              color: Colors.grey,
              fontFamily: 'Retrofont',

            ),),)
      ],
    );
  }
}