![esl project logo](https://raw.githubusercontent.com/INET-Complexity/ESL/master/project/logo/logo_card.png)


# ESL
The Economic Simulation Library (ESL) provides an extensive collection of high-performance algorithms and data structures used to develop agent-based models for economic and financial simulation. The library is designed to take advantage of different computer architectures. In order to facilitate rapid iteration during model development the library  is developed to be used from Python, and is written in C++. 

```
cd quantlib # Build and Install QuantLib, and registers it as a Conan package locally.
conan create . -s build_type=Release -s compiler.runtime=static -s compiler.runtime_type=Release --build=missing

cd ../esl/build
conan build .. -s build_type=Release -s compiler.runtime=static -s compiler.runtime_type=Release --build=missing
```


## Acknowledgements
This open-source project is organized by the Institute for New Economic Thinking at the Oxford Martin School.
Work on this open-source project is in part funded by the J.P. Morgan AI Faculty Awards 2019 and 2020.



