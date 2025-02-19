import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Arithmetic Calculator',
      theme: ThemeData(
        primarySwatch: Colors.green,
      ),
      home: CalculatorScreen(),
    );
  }
}

class CalculatorScreen extends StatefulWidget {
  @override
  _CalculatorScreenState createState() => _CalculatorScreenState();
}

class _CalculatorScreenState extends State<CalculatorScreen> {
  final TextEditingController _num1Controller = TextEditingController();
  final TextEditingController _num2Controller = TextEditingController();
  String? _operation;
  String? _result;
  String? _error;

  Future<void> _calculate() async {
    final String num1 = _num1Controller.text;
    final String num2 = _num2Controller.text;

    if (_operation == null || num1.isEmpty || num2.isEmpty) {
      setState(() {
        _error = 'Please fill in all fields and select an operation.';
      });
      return;
    }

    final String url =
        'http://110.172.151.110:8080/calculate?operation=$_operation&num1=$num1&num2=$num2';

    try {
      final response = await http.get(Uri.parse(url));
      final data = jsonDecode(response.body);

      setState(() {
        if (data['result'] != null) {
          _result = 'Result: ${data['result']}';
          _error = null;
        } else {
          _error = 'Error: ${data['error'] ?? "Unknown error"}';
          _result = null;
        }
      });
    } catch (e) {
      setState(() {
        _error = 'Error: ${e.toString()}';
        _result = null;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Arithmetic Calculator'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: _num1Controller,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(
                labelText: 'Number 1',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 10),
            TextField(
              controller: _num2Controller,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(
                labelText: 'Number 2',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 10),
            DropdownButtonFormField<String>(
              value: _operation,
              items: [
                DropdownMenuItem(
                  value: 'add',
                  child: Text('Add'),
                ),
                DropdownMenuItem(
                  value: 'subtract',
                  child: Text('Subtract'),
                ),
                DropdownMenuItem(
                  value: 'multiply',
                  child: Text('Multiply'),
                ),
                DropdownMenuItem(
                  value: 'divide',
                  child: Text('Divide'),
                ),
              ],
              onChanged: (value) {
                setState(() {
                  _operation = value;
                });
              },
              decoration: InputDecoration(
                labelText: 'Operation',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _calculate,
              child: Text('Calculate'),
            ),
            if (_result != null)
              Padding(
                padding: const EdgeInsets.only(top: 20.0),
                child: Container(
                  padding: EdgeInsets.all(10),
                  color: Colors.green[100],
                  child: Text(
                    _result!,
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 16),
                  ),
                ),
              ),
            if (_error != null)
              Padding(
                padding: const EdgeInsets.only(top: 20.0),
                child: Container(
                  padding: EdgeInsets.all(10),
                  color: Colors.red[100],
                  child: Text(
                    _error!,
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 16, color: Colors.red),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
