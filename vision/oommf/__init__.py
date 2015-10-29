import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

from . import materials
from . import geometry
from . import mifgen

oommfpath = ""

class Simulation():
    pass
    def __init__(self, geometry, cellsize, material, name="Simulation", t0=0.):
        self.geometry = geometry
        self.cellsize = cellsize
        self.material = material        
        self.name = name
        self.t = t0
        self.t0 = t0
	self.mif = ""
        self.N_mifs = 0
        self.time_series = []
    def __repr__(self): 
        cells = self.geometry.get_cells(self.cellsize)
        msg1 = "{}: {}. \n\tGeometry: {}. \n\t          Cells = {}, total={}.".format(self.name, self.material, self.geometry,
            cells, cells[0] * cells[1] * cells[2] )
        msg2 = ""
        if self.t != self.t0:
            msg2 = "\n\tCurrent t = {}s".format(self.t)
        return msg1 + msg2 

    def advance_time(self, target):
        self.mif = oommf.mifgen.assemble_mif(self)
	mifpath = oommf.mifgen.save_mif(self, target)
        oommf.run(mifpath)
        print("Integrating ODE from {}s to {}s".format(self.t, target))
        self.time_series.append([self.t, target])
        self.t = target
        
    

	        

class ImageFile(object):
    """Class for storing an image location."""

    def __init__(self, fpath):
        self.fpath = fpath
        self.format = fpath.split('.')[-1]

    def _repr_png_(self):
        if self.format == 'png':
            #return open(self.fpath, 'r').read().decode("ISO-8859-1")
            im = Image.open(self.fpath)
            return im._repr_png_()

class DataTable():
    def __init__(self, name="Simulation"):
        # read data table here
        open('tmp-data.tmp', 'w').write(example2_data)
        data = np.loadtxt("tmp-data.tmp")
        self.ts = data[:,0]
        self.m = data[:, 1:4] / 8.6e5

    def m_of_t(self):
        import seaborn
        ax = plt.subplot()
        ax.plot(self.ts, self.m)
        ax.set_xlabel('time [s]')
        ax.set_ylabel('M/Ms (A/m)')
        ax.grid('on')
        ax.set_ylim(-0.1, 1.1)
        ax.legend(['$m_x$', "$m_y$", "$m_z$"], loc='right', prop={'size':16})
        fig = ax.get_figure()
        fig.savefig("output.png", dpi=80)
        return ImageFile("output.png")


def run(mifpath, parameters = None, nice=None, pause=None, exitondone=None, kill='all'):

    bashCommand = "tclsh " + oommf.oommfpath + " boxsi"
    if parameters is not None:
        bashCommand += " -parameters " + parameters
    if nice is not None:
        bashCommand += " -nice " + nice
    if pause is not None:
        bashCommand += " -pause " + pause
    if exitondone is not None:
        bashCommand += " -exitondone " + exitondone
    if kill is not None:
        bashCommand += " -kill " + kill 
    
    bashCommand += " " + mifpath
    
    os.system(bashCommand)



def test_Simulation():
    Py = materials.permalloy
    box = geometry.Cuboid((0,0,0), (100, 30, 30))
    s = Simulation(geometry=box, cellsize=5e-9, material=Py)
    return s
    #s.m = [1, 1, 0]
    #s.advance_time(1e-





example2_data = """# 0 value for normalisation
# {Oxs_TimeDriver::Simulation_time} Oxs_TimeDriver::Mx Oxs_TimeDriver::My Oxs_TimeDriver::Mz 
9.553028888759703e-16 608105.02176463 19.26044103883042 608118.6412475563 
9.852254348931702e-15 608041.5569369476 198.6273004402372 608182.039853823 
9.271157174901216e-14 607446.924391711 1868.236062432393 608770.8339370243 
6.777597900092728e-13 603065.8084267676 13606.67246562529 612847.711220467 
1.786837210135301e-12 593897.0460937226 35554.66087901381 620241.9242730971 
3.686151550718257e-12 575730.6952184631 71945.75442063925 632086.2391472794 
5.615782081835241e-12 554337.3823443982 106929.1115400746 643385.1050481335 
6.74227595340731e-12 540592.9365016223 126237.8932634734 649773.6401599606 
7.793315675289901e-12 527011.6182148969 143456.2270504004 655629.788929499 
8.843952750867083e-12 512757.3056257872 159855.875168439 661406.8367892542 
9.888907917444863e-12 497957.0805778738 175323.5542162696 667094.2636653193 
1.093148049739221e-11 482620.7022551792 189885.6468144989 672721.3484677162 
1.197368464115913e-11 466770.417923003 203546.2863929845 678303.3154977087 
1.301262929790332e-11 450503.205146152 216249.0922183693 683823.3881625988 
1.405359149909839e-11 433789.1609852245 228041.2927865101 689303.0938865249 
1.509309866148972e-11 416737.3172578632 238867.4618696911 694713.8228842859 
1.610959435773663e-11 399767.4011341099 248524.6494087949 699933.3155815157 
1.711959278608576e-11 382670.439644299 257203.4637485431 705035.3079682272 
1.81247824544045e-11 365476.3902435983 264930.3413926761 710015.6551116048 
1.912375566250205e-11 348267.4983122492 271709.4220144369 714855.4988530723 
2.011990417471401e-11 331042.7239520741 277579.6446899507 719560.3584599398 
2.111499085809346e-11 313828.0595550541 282563.8417649314 724128.5237608618 
2.211732770069415e-11 296536.4671455738 286706.6881198734 728587.9052567059 
2.311803274974331e-11 279378.3367939219 289978.5572396286 732891.1877341924 
2.411474578200717e-11 262448.6108277539 292397.3735692524 737025.0457528104 
2.511131446129259e-11 245734.3917999858 293999.8527270542 741004.0895180536 
2.610709416791812e-11 229297.4321899405 294811.5230403391 744825.7893748281 
2.710210062107905e-11 213185.3675204997 294862.9117810751 748492.2207941647 
2.809654525432906e-11 197439.5248442993 294187.1761129677 752007.6832001123 
2.909368747030741e-11 182051.5443963994 292814.2766833678 755387.7128798722 
3.008942518242546e-11 167124.0500671681 290785.1828596172 758623.6879863621 
3.108685954122791e-11 152645.3194360161 288132.2276234297 761731.856760887 
3.208062935584133e-11 138722.3203634844 284911.6426260158 764702.6325995276 
3.307066226389139e-11 125376.5382783612 281171.2044688976 767544.029626382 
3.405351473146628e-11 112667.4155341364 276973.8823090088 770254.8499088233 
3.502807271053281e-11 100613.9761566261 272376.5863173264 772841.0365884263 
3.600443541858704e-11 89099.03152819144 267376.8492575971 775336.4486230954 
3.697923123695367e-11 78172.56208824684 262032.0808355892 777738.2347926141 
3.795712199269163e-11 67790.02777051635 256356.1289091994 780063.0166263218 
3.894081737678718e-11 57933.82595980864 250369.0458295381 782321.0703985827 
3.99185451966952e-11 48722.38443977962 244181.4625385671 784490.0151076815 
4.089978015192882e-11 40061.33089400692 237772.5299336138 786595.1693488122 
4.187912446681287e-11 31994.67004781736 231213.8280294222 788628.455786048 
4.285617149378797e-11 24514.39689173956 224544.5027286541 790592.6737073526 
4.383330864021996e-11 17590.40011473478 217782.5665733122 792495.6508004237 
4.481435299024027e-11 11187.04041437441 210933.611545025 794346.9293360583 
4.579667080612103e-11 5312.15100004041 204046.6977655463 796143.3128804018 
4.67827055244975e-11 -60.39359459889445 197134.2322279978 797890.8075438036 
4.777714171229872e-11 -4963.853928349779 190191.9296937543 799598.4652180009 
4.877251837315605e-11 -9372.764060401838 183299.3468612257 801254.3822732129 
4.97607488099642e-11 -13275.48790615883 176536.9692725163 802847.1199334274 
5.075169916343947e-11 -16735.06364424731 169859.7859966177 804394.2373272937 
5.174185637203e-11 -19759.19520007377 163313.0163968866 805891.3973888283 
5.273411481736467e-11 -22377.99285209255 156897.2177371169 807344.0903285475 
5.372038431415452e-11 -24594.66934748099 150681.4102996119 808741.9535056779 
5.470779402203687e-11 -26450.82690799767 144635.066438146 810096.5395672616 
5.569510037492388e-11 -27966.27665656468 138779.975749723 811407.195732626 
5.668340082531461e-11 -29165.11553210322 133122.0706836619 812676.4274782728 
5.767366446691022e-11 -30070.02120664182 127667.252916127 813906.3921536813 
5.866193551585305e-11 -30700.04661458797 122446.2526124883 815093.2940506814 
5.965111528460322e-11 -31080.02685662375 117450.6341827658 816241.7705809835 
6.064041908431412e-11 -31231.41183497569 112690.4863708004 817351.9413139458 
6.16322689761717e-11 -31175.5155554382 108159.364367777 818427.4490457897 
6.262241385594618e-11 -30933.5851596886 103879.9099973832 819464.7239324925 
6.361092067048076e-11 -30527.23000037787 99852.07885137976 820465.0784217411 
6.460034453078637e-11 -29975.64184790551 96065.35265900966 821432.1765062184 
6.558969728539625e-11 -29298.54033162952 92522.81219512249 822366.039677242 
6.65795266557841e-11 -28514.12563183027 89220.47781322739 823268.1785263998 
6.756565670984083e-11 -27643.97880601674 86167.94484529903 824135.941736726 
6.855308264437668e-11 -26700.99944602495 83344.63235290154 824974.8014274939 
6.953981423089521e-11 -25703.127099884 80751.38878779975 825783.9959511817 
7.052809364188192e-11 -24663.33545748205 78376.67817691524 826566.2616830582 
7.151658427194584e-11 -23597.38634869826 76217.65380326752 827321.390219153 
7.250571264444892e-11 -22518.40367249648 74266.30866895585 828050.5796119752 
7.349316879081455e-11 -21441.62967017157 72518.97104002675 828753.0604715846 
7.448184197675944e-11 -20375.74532355706 70961.90684441618 829431.7761729857 
7.547035211303247e-11 -19333.21056105714 69588.71210518292 830086.6000538714 
7.646007979901838e-11 -18322.70518650374 68388.45087165662 830719.2518380955 
7.744661274286057e-11 -17357.83129953642 67356.42902526623 831327.8095840501 
7.843364833125904e-11 -16443.1157723168 66478.28147315986 831915.4480166734 
7.942094233758047e-11 -15586.3304109864 65744.43711747862 832482.7889823716 
8.040811171634342e-11 -14794.49028005149 65145.11844721426 833030.3833502381 
8.139463138544052e-11 -14073.80706276571 64670.34050588244 833558.7200666604 
8.238028004653921e-11 -13429.35756192904 64309.78025987632 834068.4613087379 
8.336503850148128e-11 -12865.26848212174 64053.0565891667 834560.362327739 
8.435059289297847e-11 -12384.14898740715 63889.69704532804 835035.9642354583 
8.533650286453888e-11 -11989.26132924492 63810.04335341552 835495.7045076541 
8.632337044728423e-11 -11682.76657728818 63804.44979482655 835940.4914231258 
8.730870969477307e-11 -11466.95753089106 63863.32718879393 836369.8580051698 
8.829471555849396e-11 -11342.19549170511 63977.38991315581 836785.3956439749 
8.928101449443548e-11 -11309.04970110825 64137.60530749684 837187.523068696 
9.026701822446143e-11 -11367.37495834796 64335.09179914876 837576.5759615026 
9.125272664616326e-11 -11516.39959484616 64561.34226896551 837953.1194647542 
9.223621038213797e-11 -11754.31804308592 64807.69660781063 838316.9953553441 
9.322125381803098e-11 -12080.30523193034 65067.30757986438 838670.1236515719 
9.42052668164744e-11 -12491.53141244012 65332.106514956 839012.0575443244 
9.519013643923021e-11 -12986.3049743897 65595.56592231087 839343.924975498 
9.61729560415038e-11 -13560.22615958029 65850.28546792055 839665.2166982153 
9.715652512700019e-11 -14211.63147524519 66090.77548212562 839977.2974510741 
9.814094294580524e-11 -14937.34601938914 66311.18432926916 840280.5900681866 
9.912392119561689e-11 -15731.93771104654 66505.58737026251 840574.7955567756 
1.001097369115396e-10 -16595.06027628217 66669.73798173203 840861.5555308338 
1.010926236254646e-10 -17517.54687662618 66798.05308058883 841139.5615340814 
1.020777315464744e-10 -18499.8344294795 66887.02876666698 841410.6272288477 
1.030613978474639e-10 -19533.89826557232 66932.46899236839 841674.0730823963 
1.04046708009501e-10 -20618.40897979365 66931.08944323102 841931.0442835934 
1.050305644111708e-10 -21745.31563290882 66879.85434064375 842181.0406647872 
1.060142306953385e-10 -22911.2292454167 66776.19666841392 842424.6941368654 
1.069990431783039e-10 -24113.0201882754 66617.64920728491 842662.6085609189 
1.079823566889521e-10 -25342.67164707739 66402.78063053424 842894.4187443142 
1.089673109492726e-10 -26599.33492157368 66129.37743042248 843121.1203245928 
1.099500769640236e-10 -27873.37658317277 65797.36829240657 843342.0832612364 
1.109352434459834e-10 -29166.05093429289 65404.35789936271 843558.570037605 
1.119187688896309e-10 -30467.4576201109 64951.36184009036 843769.9105057861 
1.129044456495711e-10 -31778.07475635067 64436.39052620227 843977.1260169243 
1.138880233446167e-10 -33087.82229618999 63861.735661157 844179.5239401066 
1.148736407281728e-10 -34397.88854260358 63225.36691246159 844378.1440452355 
1.158577979048349e-10 -35699.43793468945 62530.11488135785 844572.456475849 
1.16843416892268e-10 -36992.29258964938 61774.81025735279 844763.2046784404 
1.178279865661353e-10 -38269.2705661536 60962.45268940854 844950.0578794745 
1.188124933624282e-10 -39527.9664225192 60093.66665336365 845133.3555768176 
1.197982608775497e-10 -40766.50110542635 59168.72685281369 845313.4739330178 
1.207820551144659e-10 -41977.48554548457 58192.44328696426 845489.9532001941 
1.217681465489025e-10 -43163.00521929666 57162.46278956105 845663.6739101952 
1.227514942132964e-10 -44314.05534092406 56086.11968026669 845833.8594983423 
1.237376976399908e-10 -45434.42708182608 54959.48245203496 846001.5764431314 
1.247217966241431e-10 -46515.88127775121 53790.4623714211 846166.0702160834 
1.257087228348241e-10 -47561.44398746304 52575.59035434165 846328.2440809424 
1.266929754161819e-10 -48563.11909538078 51324.12915425857 846487.2707313478 
1.276796965473569e-10 -49524.21408507114 50032.16175093732 846644.0494669963 
1.286645218842157e-10 -50438.69167682474 48708.01860324983 846797.9480215742 
1.296513282744247e-10 -51308.61400255248 47349.20317843516 846949.627377882 
1.306366870855607e-10 -52129.57548586779 45963.15152084248 847098.6102017021 
1.316220955512173e-10 -52901.78867472064 44550.59070773531 847245.1735485549 
1.326084078239393e-10 -53624.90602469162 43113.04217524185 847389.4820536431 
1.335933955026748e-10 -54296.56164772204 41656.54514667897 847531.248862287 
1.345800384120228e-10 -54918.19218051983 40179.45896611203 847670.9346389693 
1.355643056895719e-10 -55486.9048758035 38690.57677061863 847808.0024757149 
1.36550812286973e-10 -56005.15908330627 37185.64147912728 847943.1222606529 
1.375358227362916e-10 -56470.85861767415 35673.00704292265 848075.8059273789 
1.385222927328924e-10 -56885.50187120312 34150.76441987132 848206.4746254283 
1.395081432155819e-10 -57248.38315793526 32624.68097406571 848334.8724369491 
1.404934847960766e-10 -57560.01221090472 31097.09576455823 848461.0381411295 
1.414800953578867e-10 -57821.41133945547 29567.6841625075 848585.2162849371 
1.424654292733409e-10 -58032.53927998259 28042.7456262248 848707.1060095716 
1.43452192677113e-10 -58194.72842997052 26520.36660575335 848827.05979736 
1.44437292392954e-10 -58308.34479369882 25007.49999801367 848944.7213827686 
1.454230789526757e-10 -58374.702105608 23502.61498862467 849060.3927203523 
1.464087055320338e-10 -58394.76030408496 22009.00596580385 849173.9915976804 
1.47394425786387e-10 -58369.67095545337 20528.18329321341 849285.5664181723 
1.48379875598237e-10 -58300.67092076286 19062.48499179337 849395.0960108602 
1.493647842491425e-10 -58189.11531736074 17613.98525732319 849502.5727644351 
1.503503327232897e-10 -58036.20941628604 16182.53511081764 849608.1456671183 
1.513355775071601e-10 -57843.47133383623 14770.99633749256 849711.7340176041 
1.523215022295543e-10 -57612.12878864163 13379.3476488882 849813.4619585813 
1.533069130305103e-10 -57343.92764032045 12010.55279026686 849913.2286676798 
1.542924900506192e-10 -57040.21175258189 10664.82207192059 850011.1273432039 
1.552780958854044e-10 -56702.54435723372 9343.414034304904 850107.167931477 
1.562640012742576e-10 -56332.36577261204 8046.939621972095 850201.4007031891 
1.572496271810935e-10 -55931.45144206521 6777.022984908152 850293.7958433969 
1.582349026236081e-10 -55501.42328967505 5534.492469305004 850384.3745640238 
1.592205545275453e-10 -55043.52705102423 4319.097185577797 850473.230260214 
1.602059387814215e-10 -54559.61303190506 3132.208699104241 850560.3318920967 
1.611916734853949e-10 -54050.92135098284 1973.56643339834 850645.7615554389 
1.621763617525827e-10 -53519.72507090631 845.1766848760466 850729.4282516662 
1.631620114286425e-10 -52966.45531662109 -254.9596014242188 850811.5311011557 
1.641467926361909e-10 -52393.61745608966 -1324.566017056454 850891.9464067202 
1.651327295273993e-10 -51801.48496613686 -2365.681283662091 850970.8676191072 
1.661178990005232e-10 -51192.6254895386 -3376.178348392731 851048.1692739091 
1.671035955125503e-10 -50567.63841040585 -4357.392052624558 851123.9827561432 
1.680887541199049e-10 -49928.55222532214 -5308.321766877065 851198.2556832046 
1.690745472201504e-10 -49275.92043694345 -6230.219595357818 851271.1055522877 
1.700601083530357e-10 -48611.58159670087 -7122.437327927189 851342.4968919244 
1.71045378876874e-10 -47936.81396306933 -7985.181206646365 851412.455869474 
1.720306369121074e-10 -47252.61582852868 -8818.9951056032 851481.0319645137 
1.730159117451326e-10 -46560.10397614893 -9624.236729866636 851548.2561090959 
1.740014736170296e-10 -45860.17497509473 -10401.49007919963 851614.1747770474 
1.749863498307117e-10 -45154.56464129336 -11150.41831199062 851678.7521645495 
1.759715723514939e-10 -44443.52942110143 -11872.27167265551 851742.0845862736 
1.769565871652852e-10 -43728.41082035431 -12567.11870529593 851804.1639088747 
1.779418443041582e-10 -43009.77604432061 -13235.78509765247 851865.0457304221 
1.789275173299077e-10 -42288.34088081987 -13878.89632826533 851924.7665004742 
1.799125266333337e-10 -41565.69265386548 -14496.31080415111 851983.2878325953 
1.808984626709009e-10 -40841.41284339649 -15089.5902471 852040.7297188133 
1.818832735159065e-10 -40117.70920555753 -15658.09151733576 852096.9986660101 
1.828696092496186e-10 -39393.28875950649 -16203.93248185001 852152.27036416 
1.838547004301938e-10 -38670.79366637373 -16726.17465185667 852206.4139459239 
1.848403314129255e-10 -37949.47724829237 -17226.40439618652 852259.5525890995 
1.858256656089697e-10 -37230.47166301122 -17704.80477444842 852311.6644200284 
1.868112010469288e-10 -36513.89015787144 -18162.23933176429 852362.7989231638 
1.877968755130722e-10 -35800.21548580706 -18599.28513233263 852412.9748678808 
1.887817992266176e-10 -35090.48544994938 -19016.17860662752 852462.1698516621 
1.897674927225862e-10 -34383.96272533995 -19414.17219860632 852510.4811160498 
1.907526134243667e-10 -33681.93304216386 -19793.31706765372 852557.8635265334 
1.917383036222272e-10 -32983.86965604146 -20154.64590354636 852604.3923021049 
1.927239315803692e-10 -32290.47807877104 -20498.49420876876 852650.0567897653 
1.937095132488916e-10 -31601.9696518913 -20825.44024825269 852694.877150408 
1.946952349910207e-10 -30918.40863804865 -21136.10046891488 852738.8804861393 
1.956811026992336e-10 -30239.959215658 -21431.01253513814 852782.0849483946 
1.966666611049558e-10 -29567.07348542836 -21710.57142410748 852824.4885394806 
1.976526627239406e-10 -28899.35428496459 -21975.50000856944 852866.1406707386 
1.986380628209192e-10 -28237.60118930134 -22226.01525837656 852907.0141798223 
1.996240544574187e-10 -27581.084871667 -22462.89956396343 852947.1747589776 
2.00609518147122e-10 -26930.60474822401 -22686.34186667224 852986.5925728021 
2.015952688402255e-10 -26285.65622705933 -22896.97448614702 853025.3157575756 
2.025811933320534e-10 -25646.33723551139 -23095.18810243364 853063.3542510078 
2.035664343369583e-10 -25013.20500362675 -23281.2246621854 853100.6899761966 
2.045526401724097e-10 -24385.1950378415 -23455.77841600865 853137.3990384791 
2.055378560856687e-10 -23763.53399859548 -23618.87101263375 853173.4223789326 
2.065241773858517e-10 -23146.87179410587 -23771.19907791368 853208.8495983118 
2.075096087934607e-10 -22536.42155587806 -23912.78193502804 853243.6217141714 
2.084956538465086e-10 -21931.20506329168 -24044.15546197696 853277.8044076383 
2.094814092324869e-10 -21331.72987226451 -24165.49082516968 853311.3781716475 
2.104671388182453e-10 -20737.77812101909 -24277.1054427523 853344.363985349 
2.11453382668545e-10 -20148.97001306147 -24379.31714897074 853376.7908504794 
2.124384520468759e-10 -19566.24795647791 -24472.20680835645 853408.6149376587 
2.134250419329312e-10 -18987.95729682518 -24556.25707313137 853439.9336549164 
2.144098951596894e-10 -18415.94330114757 -24631.40870326509 853470.6543515555 
2.153966454443644e-10 -17848.03270416419 -24698.14143014454 853500.9002604086 
2.163812927676018e-10 -17286.46514942753 -24756.37457705715 853530.5589617968 
2.173679619690884e-10 -16728.82595862922 -24806.53125346812 853559.7642235459 
2.183528465045733e-10 -16177.21127518655 -24848.57726299672 853588.4126806284 
2.193392505659046e-10 -15629.71232991143 -24882.81085051965 853616.6096436017 
2.203245214173331e-10 -15087.75328711159 -24909.2759274314 853644.2879659327 
2.213105507402435e-10 -14550.24230570815 -24928.16017346273 853671.509657004 
2.222962167641836e-10 -14017.75032926206 -24939.55947304285 853698.2519451955 
2.232818827200854e-10 -13490.0391778845 -24943.59607469347 853724.5331717044 
2.242678933443202e-10 -12966.8923501151 -24940.37362501521 853750.3703244758 
2.25253110207937e-10 -12448.88164941113 -24929.99910909584 853775.7417751312 
2.262394498762914e-10 -11934.97724940589 -24912.54186161326 853800.7042808374 
2.272244017484588e-10 -11426.4673264459 -24888.13479458053 853825.2020669427 
2.282108891023153e-10 -10921.82982299947 -24856.78652282738 853849.3150079809 
2.291955627964087e-10 -10422.76915188318 -24818.68223722438 853872.9687109868 
2.301821542652375e-10 -9927.391774681895 -24773.75112850934 853896.2596844304 
2.31166836683577e-10 -9437.623399030939 -24722.23614910969 853919.1045957233 
2.321533333372016e-10 -8951.619176417378 -24664.01234120118 853941.5965490015 
2.331382085250894e-10 -8471.087761230681 -24599.34487264554 853963.6638319731 
2.341244712483183e-10 -7994.577621587529 -24528.10357049468 853985.3804374068 
2.351096341973992e-10 -7523.317022043647 -24450.52747116245 854006.6978963512 
2.360956165342907e-10 -7056.414071194577 -24366.53137236162 854027.6641300139 
2.370810659458693e-10 -6594.544661720381 -24276.28974091646 854048.256433495 
2.380666616141869e-10 -6137.424875830726 -24179.80712318965 854068.4952634624 
2.390524291112203e-10 -5685.08658129595 -24077.14158955114 854088.3869420494 
2.400377141237566e-10 -5237.87298683293 -23968.42863808358 854107.9243168271 
2.410237270736723e-10 -4795.284806411535 -23853.59893105715 854127.1370096547 
2.42008685160463e-10 -4358.171916528174 -23732.93030886808 854145.9961757939 
2.429948860638468e-10 -3925.570046066921 -23606.21010998623 854164.5512583097 
2.439796955789762e-10 -3498.691217135193 -23473.84931901774 854182.7583386939 
2.449659935759139e-10 -3076.346404415495 -23335.53538062149 854200.6759760196 
2.459507976479705e-10 -2659.87449903988 -23191.76272345418 854218.2554040282 
2.469370682455043e-10 -2248.085234365667 -23042.18014360408 854235.554685635 
2.479219290682828e-10 -1842.244582624212 -22887.30525469614 854252.5285942209 
2.489081121759038e-10 -1441.290094311639 -22726.79572050438 854269.2293139297 
2.498931247670076e-10 -1046.302542186821 -22561.14408874164 854285.619652638 
2.508790728100351e-10 -656.5005628331675 -22390.09064988595 854301.7396810027 
2.518642434083426e-10 -272.6287664356933 -22214.02591008475 854317.5662534414 
2.528499845744103e-10 105.7749559891478 -22032.80920313911 854333.1259108298 
2.53835384627045e-10 478.2937212958503 -21846.70752144489 854348.4089379839 
2.548208319269704e-10 845.0132692719409 -21655.75433457337 854363.4261554765 
2.558064220765e-10 1205.90491321142 -21460.0373307661 854378.1835577161 
2.567916529791959e-10 1560.725431980031 -21259.76819625943 854392.6782687969 
2.577774807554464e-10 1909.757765403758 -21054.86467747797 854406.9287268785 
2.587625857865436e-10 2252.477866465741 -20845.71789160578 854420.9203412808 
2.597485277388652e-10 2589.372250662163 -20632.11539712274 854434.6795430442 
2.607336196984227e-10 2919.810963018325 -20414.5439589035 854448.1871056379 
2.617195425250059e-10 3244.307864167719 -20192.75696714907 854461.4702732399 
2.627047533708401e-10 3562.305615585843 -19967.22681857308 854474.5123934672 
2.636905293123744e-10 3874.173130411431 -19737.79091295664 854487.334490119 
2.646758747213048e-10 4179.55175484245 -19504.81057164075 854499.9276042739 
2.656614543518034e-10 4478.610703987079 -19268.26225228603 854512.3042454525 
2.666469250018694e-10 4771.208870065104 -19028.36166887312 854524.4639609418 
2.676324409348375e-10 5057.360468110553 -18785.20719568262 854536.4125025964 
2.686179088177664e-10 5337.009611658558 -18538.9587348649 854548.1525074533 
2.696034119944854e-10 5610.15487526905 -18289.73354693982 854559.6886745756 
2.705888792358634e-10 5876.75489268599 -18037.68859328938 854571.0238120219 
2.715745661461273e-10 6136.859132176088 -17782.89751951441 854582.1643796886 
2.725599469009695e-10 6390.315310012516 -17525.63683677297 854593.1079845718 
2.735457494325569e-10 6637.299272469064 -17265.85693040044 854603.8661236896 
2.745311003282438e-10 6877.585491642633 -17003.92889943 854614.4326804582 
2.755169773264068e-10 7111.40903199024 -16739.7337657073 854624.8214412613 
2.765023566468139e-10 7338.52727051462 -16473.68653755671 854635.0248980203 
2.77488137451179e-10 7559.153280955356 -16205.68544436903 854645.0555921274 
2.78473669250001e-10 7773.148013746749 -15936.0469513057 854654.9100288275 
2.794592775652335e-10 7980.595949054406 -15664.82195251033 854664.5946031705 
2.804450046316197e-10 8181.51964239914 -15392.13707444352 854674.1127209226 
2.814303542497865e-10 8375.8395422913 -15118.2677989721 854683.4626463559 
2.824162311818238e-10 8563.755598179267 -14843.09910198463 854692.6558456715 
2.834015079052151e-10 8745.079393468041 -14567.08109626815 854701.6847082955 
2.843874151304753e-10 8920.067072591772 -14290.00310213202 854710.5633102534 
2.853726930153023e-10 9088.527424904316 -14012.35160207879 854719.283084332 
2.863585770533078e-10 9250.708375156217 -13733.90945735964 854727.8576694013 
2.873440515695729e-10 9406.479762312625 -13455.0924650596 854736.2808583806 
2.883297454190393e-10 9555.985214560644 -13175.85020642151 854744.5606719811 
2.893154050281038e-10 9699.229525910114 -12896.37980340561 854752.6975017067 
2.903008261701774e-10 9836.233456982689 -12616.86256306904 854760.6922323519 
2.912868947119909e-10 9967.167250910456 -12337.168426512 854768.5544180844 
2.922719709629464e-10 10091.86910450303 -12057.88140777493 854776.2734870728 
2.932582981936413e-10 10210.67706165084 -11778.4823577922 854783.8693121292 
2.942431025387783e-10 10323.31669209049 -11499.87122086803 854791.322933858 
2.952296567578986e-10 10430.22168515959 -11221.23425168859 854798.661326429 
2.962143404724534e-10 10531.06217297865 -10943.70334162926 854805.859849939 
2.972009354107691e-10 10626.29082490632 -10666.3196586422 854812.9483018287 
2.981856710966268e-10 10715.60853406953 -10390.24779347519 854819.9017649035 
2.991721380229487e-10 10799.41146970515 -10114.58280852722 854826.7476951748 
3.001570725498117e-10 10877.48963121488 -9840.336297002563 854833.465504222 
3.011433154816365e-10 10950.14252695859 -9566.813464787181 854840.0766152033 
3.021285508117345e-10 11017.26934654625 -9294.751175736812 854846.5674620395 
3.031144718290319e-10 11079.06299480851 -9023.772500525818 854852.9511977093 
3.041000233410302e-10 11135.53007734808 -8754.256767257424 854859.2228642536 
3.050856033764715e-10 11186.77301957975 -8486.180355142798 854865.3869317989 
"""
