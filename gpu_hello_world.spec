/*
A KBase module: gpu_hello_world
This sample module contains one small method that filters contigs.
*/

module gpu_hello_world {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_gpu_hello_world(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

};
