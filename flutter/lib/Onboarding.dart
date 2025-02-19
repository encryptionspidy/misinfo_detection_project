import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'LoginScreen.dart';
import 'LoginScreen.dart';

class OnboardingController extends GetxController {
  static OnboardingController get instance => Get.find();
final pageController=PageController();
Rx<int> currentPageIndex=0.obs;

  void updatePageIndicator(index)=>currentPageIndex.value=index;

  void dotNavigationCLick(index) {
    currentPageIndex.value=index;
    pageController.jumpToPage(index);
  }

  void nextPage(BuildContext context) {
    if (currentPageIndex.value == 2) {
      Navigator.pushNamed(context, '/chat');
    } else {
      int page = currentPageIndex.value + 1;
      pageController.jumpToPage(page);
      currentPageIndex.value = page;
    }
  }


  void skipPage(BuildContext context) {
    Navigator.pushNamed(context, '/chat');
    // int page=currentPageIndex.value=2;
    // pageController.jumpToPage(page);
  }

}
