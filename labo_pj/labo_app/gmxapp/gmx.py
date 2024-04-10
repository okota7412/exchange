import subprocess
import shutil
import sys
import os

def simulation(ctx):
    ensemble = ctx.get("ensemble")
    molecular_name = ctx.get("molecular_name")
    molecular_number = ctx.get("molecular_number")
    mol_kinds_num = len(molecular_name)
    temperature = float(ctx.get("temperature"))
    exe_time = float(ctx.get("exe_time"))
    exe_step = float(ctx.get("exe_step"))
    user_id = ctx.get("user_id")
    ren_path = r'/home/labo_pj/labo_app/gmxapp/ren'
    user_path = r'/home/labo_pj/labo_app/gmxapp/user_id/%s' % user_id
    cmd_list = []

    if(os.path.isdir(user_path)):
        print('Exist a folder. So remove this folder.')
        shutil.rmtree(user_path)
    

    # if文でNVT or NPT かを選択する
    if(ensemble == "NVT"):
        box_size = ctx.get("box_size")
        make_md_folders(user_path, ren_path, molecular_name)
        nvt_make_mdp_file(user_path, exe_time, exe_step, temperature) 
        cmd_list = nvt_simu(molecular_name, molecular_number, mol_kinds_num, box_size)
    elif(ensemble == "NPT"):
        box_size = ctx.get("box_size")
        pressure = float(ctx.get("pressure"))
        make_md_folders(user_path, ren_path, molecular_name)
        npt_make_mdp_file(user_path, pressure, exe_time, exe_step, temperature)
        cmd_list = npt_simu(molecular_name, molecular_number, mol_kinds_num, box_size)
    
    write_commands(user_path, cmd_list)

    # 全てのファイルを作成した後の総容量は1.5MB程度
    # os.chdir(user_path)
    # fileobj = open("gmx_command.txt", "w")
    # for cmd in range(len(cmd_list)):
    #     res = subprocess.run(cmd,stdout=subprocess.PIPE,shell=True)
    #     sys.stdout.buffer.write(res.stdout)
    #     fileobj.write(cmd + "\n")
    # fileobj.close()

    

# MDシミュレーションに必要なファイルをgmxapp/renからコピーする
def make_md_folders(user_path, ren_path, molecular_name):
    print("make_md_folders")
    os.makedirs('%s' % user_path )
    os.makedirs('%s/pdb' % user_path)
    os.makedirs('%s/input' % user_path)
    os.makedirs('%s/output' % user_path)
    
    shutil.copyfile('%s/input/md.mdp' % ren_path, '%s/input/md.mdp' % user_path)
    shutil.copytree('%s/gaff.ff' % ren_path, '%s/gaff.ff' % user_path)
    shutil.copyfile('%s/input/emin.mdp' % ren_path, '%s/input/emin.mdp' % user_path)
    shutil.copyfile('%s/input/empty.pdb' % ren_path, '%s/input/empty.pdb' % user_path)
    print("shutil.copyで input gaff をコピーしました")
    try:
        for i in range(len(molecular_name)):
            print(molecular_name[i])
            shutil.copyfile('%s/pdb/%s.pdb' % (ren_path, molecular_name[i]), '%s/pdb/%s.pdb' % (user_path, molecular_name[i]))
    except FileNotFoundError:
        print("指定されたファイルが見つかりません。")

    # shutil.copyfile('%s/input/md.mdp' % ren_path, '%s/md.gro' % user_path) #仮のmd.gro 
    # 使用する分子などのすべてのファイルはディレクトリに置いておいたほうがいいから
    # for文で使用する分子の種類に合わせてファイルをコピーするといい
    # ?.pdb, ?.itp, gaff.ff, input 
    # #付きファイルの削除方法 rm -i [#]* で確認しながら削除できる

# NPT アンサンブルに合わせてmd.mdpを編集
def npt_make_mdp_file(user_path, pressure, exe_time, exe_step, temperature):
    print("make npt_mdp file")

    with open(f'{user_path}/input/md.mdp', 'a') as fout:
            nsteps = (exe_time*1000)/(exe_step*0.001)
            dt = exe_step*0.001
            ref_t = temperature+273.15
            ref_p = pressure*1.013
            # print('nsteps = %d' % nsteps)
            # print('dt = %f' %dt)
            # print('ref_t = %f' % ref_t)
            # print('ref-p = %f' % ref_p)
            fout.write('pcoupl = parrinello-rahman\n')
            fout.write('pcoupltype = isotropic\n')
            fout.write('ref-p = %f %f\n' % (ref_p, ref_p))
            fout.write('nsteps = %d\n' % nsteps)
            fout.write('dt = %f\n' % dt)
            fout.write('ref_t = %f'% ref_t)

# NVT アンサンブルに合わせてmd.mdpを編集
def nvt_make_mdp_file(user_path, exe_time, exe_step, temperature):
    print("make nvt_mdp file")

    with open(f'{user_path}/input/md.mdp', 'a') as fout:
            nsteps = (exe_time*1000)/(exe_step*0.001)
            dt = exe_step*0.001
            ref_t = temperature+273.15
            # print('nsteps = %d' % nsteps)
            # print('dt = %f' %dt)
            # print('ref_t = %f' % ref_t)
            fout.write('pcoupl = no\n')
            fout.write('nsteps = %d\n' % nsteps)
            fout.write('dt = %f\n' % dt)
            fout.write('ref_t =%f'% ref_t)

# NVTモデルのMDシミュレーション
def nvt_simu(molecular_name, molecular_number, mol_kinds_num, box_size):
    cmd_list =[]

    # コマンドを実行するためにファイルコピーをしておく　*.pdb gaff, input, output folder 

    #insertm-molecules
    cmd_list.append('gmx insert-molecules -f ./input/empty.pdb -ci ./pdb/%s.pdb -nmol %s -box %s %s %s -o ./output/box.pdb' % (molecular_name[0], molecular_number[0], box_size[0], box_size[1], box_size[2]))#分子の種類が1個の場合
    for i in range(mol_kinds_num - 1):
        cmd_list.append('gmx insert-molecules -f ./output/box.pdb -ci ./pdb/%s.pdb -nmol %s -box %s %s %s -o ./output/box.pdb' % (molecular_name[i+1], molecular_number[i+1], box_size[0], box_size[1], box_size[2])) #分子の種類が複数の場合 
    #pdb2gmx 
    cmd_list.append('gmx pdb2gmx -f ./output/box.pdb -o ./output/conf.gro -p topol.top -i posre.itp -ff gaff -water tip3p')
    #editconf
    cmd_list.append('gmx editconf -f ./output/conf.gro -o ./output/conf_box.gro -box %s %s %s' % (box_size[0], box_size[1], box_size[2]))
    #grompp
    cmd_list.append('gmx grompp -f ./input/emin.mdp -c ./output/conf_box.gro -p topol.top -o ./output/emin.tpr -po ./output/mdout.mdp')
    #mdrun
    cmd_list.append('gmx mdrun -s ./output/emin.tpr -deffnm ./output/emin -v')
    # grompp after mdrun
    cmd_list.append('gmx grompp -f ./input/md.mdp -c ./output/emin.gro -p topol.top -o ./output/md.tpr')
    # mdrun after emin
    cmd_list.append('gmx mdrun -s ./output/md.tpr -deffnm ./output/md -v')
    
    # calculate rdf
    # cmd_list.append('gmx rdf -f ./output/md.xtc -s ./output/md.tpr -o ./output/rdf.xvg')
    # -ref -sel を設定しなければいけないが何を示しているのかが分からないために設定できていない

    # 作成したコマンドリストを返す
    return cmd_list
        


# NPTモデルのMDシミュレーション
def npt_simu(molecular_name, molecular_number, mol_kinds_num, box_size):
    cmd_list =[]

    # コマンドを実行するためにファイルコピーをしておく　*.pdb gaff, input, output folder 

    #insertm-molecules
    cmd_list.append('gmx insert-molecules -f ./input/empty.pdb -ci ./pdb/%s.pdb -nmol %s -box %s %s %s -o ./output/box.pdb' % (molecular_name[0], molecular_number[0], box_size[0], box_size[1], box_size[2]))#分子の種類が1個の場合
    for i in range(mol_kinds_num - 1):
        cmd_list.append('gmx insert-molecules -f ./output/box.pdb -ci ./pdb/%s.pdb -nmol %s -box %s %s %s -o ./output/box.pdb' % (molecular_name[i+1], molecular_number[i+1], box_size[0], box_size[1], box_size[2])) #分子の種類が複数の場合 
    #pdb2gmx 
    cmd_list.append('gmx pdb2gmx -f ./output/box.pdb -o ./output/conf.gro -p topol.top -i posre.itp -ff gaff -water tip3p')
    #editconf
    cmd_list.append('gmx editconf -f ./output/conf.gro -o ./output/conf_box.gro -box %s %s %s' % (box_size[0], box_size[1], box_size[2]))
    #grompp
    cmd_list.append('gmx grompp -f ./input/emin.mdp -c ./output/conf_box.gro -p topol.top -o ./output/emin.tpr -po ./output/mdout.mdp')
    #mdrun
    cmd_list.append('gmx mdrun -s ./output/emin.tpr -deffnm ./output/emin -v')
    # grompp after mdrun
    cmd_list.append('gmx grompp -f ./input/md.mdp -c ./output/emin.gro -p topol.top -o ./output/md.tpr')
    # mdrun after emin
    cmd_list.append('gmx mdrun -s ./output/md.tpr -deffnm ./output/md -v')
    
    # calculate rdf
    # cmd_list.append('gmx rdf -f ./output/md.xtc -s ./output/md.tpr -o ./output/rdf.xvg')
    # -ref -sel を設定しなければいけないが何を示しているのかが分からないために設定できていない

    # 作成したコマンドリストを返す
    return cmd_list

# コマンドを順次書き込む関数
def write_commands(path, cmd_list):
    if(isinstance(cmd_list, list)):
        for cmd in cmd_list:
            try:
                # 実行したコマンドリストをファイルに書き込む
                with open(f'{path}/gmx_command.txt', mode="a") as f:
                    f.write(cmd + "\n")

            except Exception as e:
                # エラーが発生した場合
                return {"error": e} 
    else:
        try:
            # 実行したコマンドリストをファイルに書き込む
            with open(f'{path}/gmx_command.txt', mode="a") as f:
                f.write(cmd_list + "\n")

        except Exception as e:
            # エラーが発生した場合
            return {"error": e} 
    
    # for cmd in cmd_list:
    #     try:
    #         # コマンドを実行して標準出力と標準エラー出力を取得
    #         res = subprocess.run(cmd, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #         sys.stdout.buffer.write(res.stdout)
    #         # 実行したコマンドリストをファイルに書き込む
    #         with open(f'{path}/gmx_command.txt', mode="a") as f:
    #             f.write(cmd + "\n")

    #     except subprocess.CalledProcessError as e:
    #         # エラーが発生した場合
    #         print(f"Command failed with return code {e.returncode}")
    #         return {"error": e.stderr}  # エラーが発生したら stderr を返す

# msdコマンドを書き込む
def write_msd(path, msd_mol, exe_time):
    # 全体の計算時間の頭10%を除いて、MSDを実行させる
    b_op = int(exe_time * 0.1 * 1000)
    print("b_op = ",b_op)
    cmd = f'echo {msd_mol} | gmx msd -f ./output/md.xtc -s ./output/md.tpr -o ./output/{msd_mol}_msd.xvg -b {b_op}'
    write_commands(path, cmd)

# rdfコマンドを書き込む
def write_rdf(path, ref_mol, sel_mol, exe_time):
    # 全体の計算時間の頭10%を除いて、RDFを実行させる
    b_op = int(exe_time * 0.1 * 1000)
    cmd = f'gmx rdf -f ./output/md.xtc -s ./output/md.tpr -o ./output/{ref_mol}-{sel_mol}_rdf.xvg -selrpos mol_com -seltype mol_com -ref {ref_mol} -sel {sel_mol} -b {b_op}'
    write_commands(path, cmd)

# rdf.xvgファイルのデータだけを抽出してJSONで返す関数(左の列がx, 右の列がy)
def read_rdf(path, ref_mol, sel_mol):
    try:
        x = []
        y = []
        with open(f'{path}/output/{ref_mol}-{sel_mol}_rdf.xvg', 'r') as file:
            for line in file:
                # 行がコメント行でない場合のみ追加
                if not line.strip().startswith('#') and not line.strip().startswith('@') and line:
                    x.append(line.strip().split()[0])
                    y.append(line.strip().split()[1])
            # print("x = ",x)
            # print("y = ",y)
        return {"x": x, "y": y}
    except Exception as e:
        return {"error": e}
    
# msd.xvgファイルのデータだけを抽出してJSONで返す関数(左の列がx, 右の列がy)
def read_msd(path, msd_mol):
    try:
        x = []
        y = []
        with open(f'{path}/output/{msd_mol}_msd.xvg', 'r') as file:
            lines = file.readlines()
            for line in lines[20:]:
                x.append(line.strip().split()[0])
                y.append(line.strip().split()[1])
        return {"difCoe":lines[19], "x": x, "y": y}
    except Exception as e:
        return {"error": e}
        


# gztar圧縮 ***二重圧縮になる可能性が高い***
def gmx_gztar(user_id):
    gztar_path = r'/home/labo_pj/labo_app/gmxapp/user_id/%s' % user_id
    #print(gztar_path)
    if(os.path.exists('%s/gmx.tar.gz' % gztar_path)):
        print("tar.gzファイルは存在しているので削除します。")
        os.remove('%s/gmx.tar.gz' % gztar_path)
        print("type=delete "+os.getcwd())
        os.chdir(gztar_path)
        shutil.make_archive('gmx', format='gztar', root_dir=gztar_path)
        #shutil.move('/home/labo_pj/gmx.tar.gz', gztar_path)
    else:
        print("新規でtar.gzファイルを作成します")
        os.chdir(gztar_path)
        shutil.make_archive('gmx', format='gztar', root_dir=gztar_path)
        print("type=new "+os.getcwd())
        #shutil.move('/home/labo_pj/gmx.tar.gz', gztar_path)
        # shutil.make_archive('gmx', base_dir=gztar_path, format='gztar', root_dir=gztar_path)
