import json
import os
import subprocess
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from json.decoder import JSONDecodeError
from socketserver import ThreadingMixIn
import gc
import shutil
import subprocess
import sys
import time
import traceback

class Handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        pass

    def do_GET(self):
        pass
    def do_POST(self):
        content_len  = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_len ).decode()

        try:
            body_content = json.loads(post_body)
        except JSONDecodeError:
            print('JSONDecodeError, post_body не было загружено должным образом.')
        else:
            problem_name, student_response, hide_answer = get_info(body_content)
        if hide_answer == "True":
                hide_answer = True
        else:
                hide_answer = False
        result = grade(problem_name, student_response, hide_answer)
      
        send = json.dumps(result).encode()
    
        self.send_response(200)
        self.end_headers()
        self.wfile.write(send)
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ 
        Этот класс позволяет обрабатывать запросы в различных потоках. 
    """

def grade(problem_name, student_response, hide_answer):

    source_file = open("/edx/my-grader/Program.java", 'w')
    source_file.write(student_response)
    source_file.close()
    result = {}
    p = subprocess.Popen(["javac", "Program.java"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if (err):
        result.update({"correct": False, "error": (err)})
        result = create_response(result, hide_answer) 
        return result

 
    test_runner_java = "/edx/my-grader/" + problem_name + ".java"
    p = subprocess.Popen(["javac", "-classpath", "/edx/my-grader:/edx/my-grader/junit-4.11.jar:/edx/my-grader/hamcrest-core-1.3.jar", test_runner_java], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    print(err)
    p = subprocess.Popen(["java","-classpath", "/edx/my-grader:/edx/my-grader/junit-4.11.jar:/edx/my-grader/hamcrest-core-1.3.jar", problem_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    out = out.decode('utf-8')
    if (err):
        result.update({"correct": False, "error": (err)})
        result = create_response(result, hide_answer)
        return result
    out = re.split("\n", out)
    keys = ['correct', 'function', 'result', 'expected']
    out1 =[];
    result =[];
    for i in range(len(out)-1):
        out1 = re.split(" ", out[i])
        result.append(dict(zip(keys, out1))) 
    
    return create_response(result, hide_answer)

def create_response(result, hide_answer): 
    
    
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
        result = [{'correct':False, 'error': "No result"}]
    for i in range(len(result)):
        if result[i]['correct']=="true" :
                result[i]['correct']= True
        else :
                result[i]['correct']= False 
    number_passed = sum(r['correct'] for r in result)
    out["correct"] = (number_passed == len(result))

    print(number_passed)
    out["score"] = number_passed / len(result)


    if any(('error' in res) for res in result):
        html_message = start.format('ERROR')

    elif out['correct']:
        html_message = start.format('CORRECT')

    else:
        html_message = start.format('INCORRECT')

    
    for i, res in enumerate(result):
        
        answer = {'correct': False, 'function': "", 'result': "", 'expected': ""}
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
    #print(out)
    return out


def get_info(json_object):
    json_object = json.loads(json_object['xqueue_body'])
    grader_payload = json.loads(json_object['grader_payload'])
    student_response = json_object['student_response']
    student_id = json.loads(json_object['student_info']).get('anonymous_student_id', 'unknown')
    problem_name = grader_payload['problem_name']
    hide_answer = grader_payload['hide_answer']
    return problem_name, student_response, hide_answer

if __name__ == "__main__":

    server = ThreadedHTTPServer(("localhost", 1710), Handler)
    server.serve_forever()
