import 'package:flutter/material.dart';

class ScreenHelper {
  static double screenWidth(BuildContext context) {
    return MediaQuery.of(context).size.width;
  }

  static double screenHeight(BuildContext context) {
    return MediaQuery.of(context).size.height;
  }

  static double screenPercentageWidth(BuildContext context, double percentage) {
    return screenWidth(context) * percentage;
  }

  static double screenPercentageHeight(BuildContext context, double percentage) {
    return screenHeight(context) * percentage;
  }
}
