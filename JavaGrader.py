import BaseHTTPServer
import json
import os
import subprocess
import re

class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_POST(self):
        body_len = int(self.headers.getheader('content-length', 0))
        body_content = self.rfile.read(body_len)
        problem_name, student_response, hide_answer = get_info(body_content)
        if hide_answer == "True":
                hide_answer = True
        else:
                hide_answer = False
        result = grade(problem_name, student_response, hide_answer)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(result)

def grade(problem_name, student_response, hide_answer):

    source_file = open("/edx/my-grader/Program.java", 'w')
    source_file.write(student_response)
    source_file.close()
    result = {}
    p = subprocess.Popen(["javac", "/edx/my-grader/Program.java"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    if (err != ""):
        result.update({"correct": False, "error": (err)})
        result = create_response(result, hide_answer) 
        return result

 
    test_runner_java = "/edx/my-grader/" + problem_name + ".java"
    p = subprocess.Popen(["javac", "-classpath", "/edx/my-grader:/edx/my-grader/junit-4.11.jar:/edx/my-grader/hamcrest-core-1.3.jar", test_runner_java], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    p = subprocess.Popen(["java", "-classpath", "/edx/my-grader:/edx/my-grader/junit-4.11.jar:/edx/my-grader/hamcrest-core-1.3.jar", problem_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if (err != ""):
        result.update({"correct": False, "error": (err)})
        result = create_response(result, hide_answer)
        return result
    out = re.split("\n", out)
    keys = ["correct", "function", "result", "expected"]
    out1 =[];
    result =[];
    for i in range(len(out)):
        out1 = re.split(" ", out[i])
        result.append(dict(zip(keys, out1))) 
    create_response(result, hide_answer)
    return result

def create_response(result, hide_answer):  
    print(result[0]["correct"])
    for i in range(len(result)-1):
        if result[i]["correct"] == "True":
                result[i]["correct"] = True
        else:
                result[i]["correct"]= False
     print(result)
    start = """
            <div class="test">
                <header>Test results</header>
                <section>
                    <div class="shortform">
                    {}
                    <a href="#" class="full full-top">See full test results</a>
                    </div>
            <div class="longform" style="display: none;">
            """

    end = """</div></section></div>"""

    correct =  """
                <div class="result-output result-correct">
                    <h4>{header}</h4>
                    <pre>{function}</pre>
                    <dl>
                        <dt>Output:</dt>
                        <dd class="result-actual-output"><pre>{result}</pre></dd>
                    </dl>
                </div>
                """
    
    correct_hidden =  """
                <div class="result-output result-correct">
                    <h4>{header}</h4>
                </div>
                """
    wrong = """
            <div class="result-output result-incorrect">
                    <h4>{header}</h4>
                    <pre>{function}</pre>
                    <dl>
                        <dt>Your output:</dt>
                        <dd class="result-actual-output"><pre>{result}</pre></dd>
                        <dt>Correct output:</dt>
                        <dd><pre>{expected}</pre></dd>
                    </dl>
            </div>
            """
    wrong_hidden = """
            <div class="result-output result-incorrect">
                    <h4>{header}</h4>
            </div>
            """

    fatal = """
            <div class="result-output result-incorrect">
                <h4>Error</h4>
                <dl>
                <dt>Message:</dt>
                <dd class="result-actual-output"><pre>{error}</pre></dd>
                </dl>
            </div>
            """

    out = {}

    
    if isinstance(result, dict):
        result = [result]
    
    if not result:
        result = [{"correct":False, "error": "No result"}]

    
    number_passed = sum(r["correct"] for r in result)
    out["correct"] = (number_passed == len(result))

    
    out["score"] = number_passed / len(result)

   
    if any(("error" in res) for res in result):
        html_message = start.format("ERROR")
    elif out["correct"]:
        html_message = start.format("CORRECT")
    else:
        html_message = start.format("INCORRECT")

    
    for i, res in enumerate(result):
        
        answer = {"correct": False, "function": "", "result": "", "expected": ""}
        answer.update(res)

        if "error" in res:
            html_message += fatal.format(**answer)
        else:
            name = "Test Case {}".format(i+1)
            if hide_answer:
                if res["correct"]:
                    html_message += correct_hidden.format(header=name)
                else:
                    html_message += wrong_hidden.format(header=name)
            else:
                if res["correct"]:
                    html_message += correct.format(header=name, **answer)
                else:
                    html_message += wrong.format(header=name, **answer)

    
    html_message += end
    out["msg"] = html_message

    return out


def get_info(body_content):
    json_object = json.loads(body_content)
    json_object = json.loads(json_object["xqueue_body"])
    grader_payload = json.loads(json_object["grader_payload"])
    student_response = json_object["student_response"]
    problem_name = grader_payload["problem_name"]
    hide_answer = grader_payload["hide_answer"]
    return problem_name, student_response, hide_answer

if __name__ == "__main__":

    server = BaseHTTPServer.HTTPServer(("localhost", 1710), HTTPHandler)
    server.serve_forever()
