# Makefile
CXX=g++
CXXFLAGS=-std=c++17 -O2 -I/Users/ozgurakgun/Downloads/or-tools_arm64_macOS-14.1_cpp_v9.8.3296/include
LDFLAGS=-L/Users/ozgurakgun/Downloads/or-tools_arm64_macOS-14.1_cpp_v9.8.3296/lib -lortools

native: native.cpp
	$(CXX) $(CXXFLAGS) native.cpp $(LDFLAGS) -o native
