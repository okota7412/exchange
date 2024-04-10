import json,os,re,subprocess,sys,time
from .gmxapp import gmx
from django.http import JsonResponse


# Ajax通信を使ったgmxコマンドを実行する関数
def ajax_exe_gmx_com(request):
    post_data = json.loads(request.body.decode('utf-8')) # POSTデータをJSONからPythonオブジェクトにパース
    user = getattr(request, "user", None)
    user_id = user.id
    molecular_name = remove_sp_char(post_data.get("molecular_name"))
    molecular_number = remove_sp_char(post_data.get("molecular_number"))
    if(not isinstance(molecular_name, list)):
        molecular_name = [molecular_name]
        molecular_number = [molecular_number]
    box_size = remove_sp_char(post_data.get("box_size"))
    pressure = remove_sp_char(post_data.get("pressure"))
    ensemble = remove_sp_char(post_data.get("ensemble"))
    temperature = remove_sp_char(post_data.get("temperature"))
    exe_time = remove_sp_char(post_data.get("exe_time"))
    exe_step = remove_sp_char(post_data.get("exe_step"))
    
    ctx = {"ensemble": ensemble,
           "molecular_name": molecular_name,
           "molecular_number": molecular_number,
           "pressure": pressure,
           "temperature": temperature,
           "exe_time": exe_time,
           "exe_step": exe_step,
           "box_size": box_size,
           "user_id": user_id,
           }
    print(ctx)

    start = time.time()
    # ここでシミュレーションを実行させる
    gmx.simulation(ctx)
    path = f"/home/labo_pj/labo_app/gmxapp/user_id/{user_id}"
    result = execute_lines_without_last(path)
    # finish = time.time()
    # elapsed_t = finish - start
    # elapsed_t = int(elapsed_t)
    # result["elapsed_t"] = elapsed_t

    return JsonResponse(result)

# 最後の行を実行してresponseを返す
def ajax_heavy_task(request):
    user = getattr(request, "user", None)
    user_id = user.id
    path = f"/home/labo_pj/labo_app/gmxapp/user_id/{user_id}"
    result = execute_last(path)
    return JsonResponse(result)

# fetchData()
def get_output(request):
    post_data = json.loads(request.body.decode('utf-8')) # POSTデータをJSONからPythonオブジェクトにパース
    user_id = post_data.get('user_id')  # フォームから送られたコマンドを取得
    path = f'/home/labo_pj/labo_app/gmxapp/user_id/{user_id}'
    try:
        with open(f'{path}/result.txt', 'r', encoding='utf-8') as file:
            file_content = file.read()
        # fileの内容を毎回そのまま送っているからデータの送信料が多くなる
        # 差分だけ送る方法があればいいかな   
        return JsonResponse({'content': file_content})
    except FileNotFoundError:
        return JsonResponse({'error': 'ファイルが見つかりません。'})
    except Exception as e:
        return JsonResponse({'error': f'エラーが発生しました: {str(e)}'})

# msdコマンドを実行させる関数
def ajax_msd(request):
    post_data = json.loads(request.body.decode('utf-8')) # POSTデータをJSONからPythonオブジェクトにパース
    user = getattr(request, "user", None)
    user_id = user.id
    msd_mol = name_for_analysis(remove_sp_char(post_data.get("msd_mol")))
    exe_time = post_data.get("exe_time")

    if(msd_mol==-1):
        print("msd_mol エラー")
        return JsonResponse({"error": "msd_name error"})
    else:
        path = f'/home/labo_pj/labo_app/gmxapp/user_id/{user_id}'
        if (not os.path.exists(f'{path}/output/{msd_mol}_msd.xvg')):
            gmx.write_msd(path, msd_mol, exe_time) #(gmx内のmsdのコマンドを書き込む関数を呼び出す)
            result = execute_last(path) #書き込んだmsdのコマンドを実行する
            if('error' in result):
                print("rdf error")
                return JsonResponse(result)
        
        result = gmx.read_msd(path,msd_mol)
        # print(result)
        return JsonResponse(result)

# rdfコマンドを実行させる関数
def ajax_rdf(request):
    post_data = json.loads(request.body.decode('utf-8')) # POSTデータをJSONからPythonオブジェクトにパース
    user = getattr(request, "user", None)
    user_id = user.id
    ref_mol = name_for_analysis(remove_sp_char(post_data.get("ref_mol")))
    sel_mol = name_for_analysis(remove_sp_char(post_data.get("sel_mol")))
    exe_time = post_data.get("exe_time")

    if(ref_mol==-1 or sel_mol==-1):
        print("ref_mol or sel_mol エラー")
        return JsonResponse({"error": "rdf_name error"})
    else:
        path = f'/home/labo_pj/labo_app/gmxapp/user_id/{user_id}'
        if (not os.path.exists(f'{path}/output/{ref_mol}-{sel_mol}_rdf.xvg')):
            gmx.write_rdf(path, ref_mol, sel_mol, exe_time) #(gmx内のrdfのコマンドを書き込む関数を呼び出す)
            result = execute_last(path) #書き込んだrdfのコマンドを実行する
            if('error' in result):
                print("rdf error")
                return JsonResponse(result)
        
        result = gmx.read_rdf(path, ref_mol, sel_mol)
        # print(result)
        return JsonResponse(result)

    # try:
    #     with open(f'{path}/output/md.xvg', 'r', encoding='utf-8') as file:
    #         file_content = file.read()  
    #     return JsonResponse({'content': file_content})
    # except FileNotFoundError:
    #     return JsonResponse({'error': 'ファイルが見つかりません。'})
    # except Exception as e:
    #     return JsonResponse({'error': f'エラーが発生しました: {str(e)}'})


# 最後の一行以外を実行する関数
def execute_lines_without_last(path):
    try:
        with open(f'{path}/gmx_command.txt', 'r', encoding='utf-8') as file:
            # ファイルの各行を読み込み
            lines = file.readlines()

            # 最後の行以外のコマンドを実行
            for line in lines[:-1]:
                cmd = line.strip()
                print(f"Executing command: {cmd}")

                try:
                    # コマンドの実行
                    res = subprocess.run(cmd, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    # sys.stdout.buffer.write(res.stdout)
                    # 実行結果を表示
                    print(f"Command output:\n{res.stdout.decode('utf-8')}")
                    if res.returncode != 0:
                        print(f"Command failed with return code {res.returncode}")
                        print(f"Command error: {res.stderr.decode('utf-8')}")
                        return {"error": res.stderr.decode('utf-8')}

                except subprocess.CalledProcessError as e:
                    return {"error": e}

            print('Execution completed.')
            return {}
    except Exception as e:
        print(f"Error reading or executing commands: {e}")
        return {"error": e}


# 各ユーザのフォルダ内のgmx_command.txtを読み込んで全体の長さ-1までコマンドを実行させればgmx mdrun mdだけ後で実行できそう
# 最後の行を実行する関数
def execute_last(path):
    try:
        with open(f'{path}/gmx_command.txt', 'r', encoding='utf-8') as file:
            # ファイルの最後の行を読み取る
            last_line = file.readlines()[-1].strip()
            cmd = f"{last_line} 2> result.txt"

            try:
                # コマンドの実行
                res = subprocess.run(cmd, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                # sys.stdout.buffer.write(res.stdout)
                # 実行結果を表示
                print("execute_last")
                print(f"Command output:\n{res.stdout.decode('utf-8')}")
                if res.returncode != 0:
                    print(f"Command failed with return code {res.returncode}")
                    print(f"Command error: {res.stderr.decode('utf-8')}")
                    # return {"error": res.stderr.decode('utf-8')}
                    return {"error": res.returncode}
            except subprocess.CalledProcessError as e:
                return {"error": e}

            print('Execution completed.')
            return {}
    except Exception as e:
        print(f"Error reading or executing commands: {e}")
        return {"error": e}

# 特殊文字を取り除く関数
def remove_sp_char(user_str):
    if(isinstance(user_str, list)):
        return [remove_sp_char(item) for item in user_str]
    else:
        code_regex = re.compile('[\s!"#$%&\'\\\\()+,\:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]')
        cleaned_str = code_regex.sub('', user_str)
        return cleaned_str

# gmxの解析で扱う名前を返す関数
def name_for_analysis(mol_name):
    match mol_name:
        case "水":
            return "Water"
        case "アセチレン":
            return "C2H2"
        case "アセトン":
            return "C2CO"
        case "アンモニア":
            return "NH3"
        case "エタノール":
            return "C2O"
        case "エチレン":
            return "C2H4"
        case "シクロブタン":
            return "C4H8"
        case "ベンゼン":
            return "C6H6"
        case "メタノール":
            return "CH4O"
        case "塩化水素":
            return ""
        case "酢酸":
            return "C2O2"
        case _:
            print("not matched")
            return -1

# Ajax通信を使った送信されたコマンドを実行する例
def ajax_exe_com(request):
    post_data = json.loads(request.body.decode('utf-8')) # POSTデータをJSONからPythonオブジェクトにパース
    command = post_data.get('command')  # フォームから送られたコマンドを取得
    print(command)
    os.chdir('/home/labo_pj/labo_app/gmxapp/user_id/5')

    command = command + " 2> result.txt"
    print(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    result = {
        'command': command,
        'output': output.decode('utf-8'),
        'error': error.decode('utf-8')
    }
    print(output.decode('utf-8'))

    return JsonResponse({'results': result})

    

# def get_output(request):
#     os.chdir('/home/labo_pj/labo_app/gmxapp/user_id/3')
#     try:
#         with open('result.txt', 'r', encoding='utf-8') as file:
#             file_content = file.read()
#             count1 = sum(1 for line in file)
#             print("行数1", count1)
#         with open('pre_result.txt', 'a+', encoding='utf-8') as pre_file:
#             count2 = sum(1 for line in pre_file)
#             print("行数2", count2)
#             selected_lines = lines[count-1:end_line]

#         # fileの内容を毎回そのまま送っているからデータの送信料が多くなる
#         # 差分だけ送る方法があればいいかな   
#         return JsonResponse({'content': file_content})
#     except FileNotFoundError:
#         return JsonResponse({'error': 'ファイルが見つかりません。'})
#     except Exception as e:
#         return JsonResponse({'error': f'エラーが発生しました: {str(e)}'})


# フォームから送信されたコマンドの実行結果を保持する変数
# command_output = ""
# result = ""

# コマンドの実行を待ってから結果を出力してしまうから一旦コメントアウト
# def execute_command(request):
#     global command_output
#     os.chdir('/home/labo_pj/labo_app/gmxapp/user_id/3')
#     global result
#     if request.method == 'POST':
#         try:
#             # フォームから送信されたコマンドを取得
#             post_data = json.loads(request.body.decode('utf-8')) # POSTデータをJSONからPythonオブジェクトにパース
#             command = post_data.get('command')  # フォームから送られた複数のコマンドのリストを取得
#             print(command)

#             # 外部コマンドを実行
#             result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             print("コマンドを実行しました")
#             output = result.stdout.decode('utf-8')
#             error = result.stderr.decode('utf-8')

#             # コマンドの実行結果を保持
#             command_output = f'Output: {output}\nError: {error}'
#             return JsonResponse({'output': command_output})
#         except Exception as e:
#             # エラーが発生した場合の処理
#             command_output = f'Error: {str(e)}'
#             return JsonResponse({'output': command_output})
#     else:
#         # POSTリクエストでない場合やAjaxリクエストでない場合はエラーメッセージを返す
#         return JsonResponse({'error': 'Invalid request'})

# リアルタイムのコマンド実行のやり方
# def execute_command(request):
#     # global command_output
#     os.chdir('/home/labo_pj/labo_app/gmxapp/user_id/3')
#     # global result
#     if request.method == 'POST':
#         # フォームから送信されたコマンドを取得
#         post_data = json.loads(request.body.decode('utf-8')) # POSTデータをJSONからPythonオブジェクトにパース
#         command = post_data.get('command')  # フォームから送られた複数のコマンドのリストを取得
#         print(command)
        
#         async def run_command():
#             process = await asyncio.create_subprocess_shell(
#                 command,
#                 stdout=asyncio.subprocess.PIPE,
#                 stderr=asyncio.subprocess.PIPE
#             )

#             stdout, stderr = await process.communicate()

#             # サブプロセスの標準出力と標準エラー出力を取得
#             return stdout.decode(), stderr.decode()

#         # 非同期処理を同期的に実行
#         stdout, stderr = asyncio.run(run_command())
#         print(stdout, stderr)
#         # コマンドのリアルタイムな実行結果をJSONで返す
#         return JsonResponse({'stdout': stdout, 'stderr': stderr})
        
#     else:
#         # POSTリクエストでない場合やAjaxリクエストでない場合はエラーメッセージを返す
#         return JsonResponse({'error': 'Invalid request'})



# def get_output(request):
#     global command_output
#     global result
#     # コマンドの実行結果をJSON形式で返す
#     # return JsonResponse({'output': command_output})    
#     return JsonResponse({'output': result.stdout.decode('utf-8')})    

