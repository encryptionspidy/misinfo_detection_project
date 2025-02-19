import 'package:flutter/material.dart';

class Utility{
  static const double defaultSpace = 8.0;

  static double bottomNavigationdefaultHeight = 56.0;

  static double getAppBarHeight(){
    return kToolbarHeight;
  }

  static bool isDarkMode(BuildContext context){
    return Theme.of(context).brightness==Brightness.dark;
  }



}
