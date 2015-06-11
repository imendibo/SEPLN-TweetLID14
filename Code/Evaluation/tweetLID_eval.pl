#!/bin/perl

#
# tweetLID_eval.pl : tweetLID 2014 Twitter Language Identification shared task evaluation script. Computes the P/R/F values per category of a result file against a reference.
#
# Author : Iñaki San Vicente (i.sanvicente@elhuyar.com)
#
# Last Update: 2014/06/30 
#                     - line 260: Corrected bug when evaluating "lang1+lang2[+lang3]" type annotations.
#


my $usage = <<"_USAGE_"; 

  NAME: tweetLID_eval.pl 
  
  Arguments:
        1. --reference=|-r: path to the file containing the gold standard reference. 
                        BY DEFAULT it looks for the \'tweetLID-training_ids.tsv\' file in this directory.

                        IMPORTANT: Reference file format is: \'tweetId<tab>userId<tab>language\'

        2. --data=|-d: User provided result file. 
                       Required file format is: \'tweetId<tab>language\' 
                       where \'language\' accepts the folowing strings: 
                                - \'lang1\': single language. Possible values are: [es,en,gl,ca,eu,pt,und,other]
                                - \'lang1+lang2[+lang3]\': multiple languages. Any combination of the abovementioned codes are allowed.
                       IMPORTANT: 
                          - \'lang1/lang2/lang3\' type answer is not allowed. If such notation is found only the first language will be taken into account.
                          - When using multiple languages, \'lang1+lang2[+lang3]\' a maximun number of 3 languages may be included. If more are found only the first 3 languages will be taken into account.
 
        3. --help|-h : print this help.

  Output: 
         Standard output. Precision and Accuracy results obtained by the entered input

    Example calls:
           \$ perl tweetLID_eval -d runToEvaluate.txt ---- standard output
           \$ perl tweetLID_eval -d runToEvaluate.txt -r customReferenceFile.txt ---- standard output

_USAGE_


#############################################################
#
#          Main Program
#
#############################################################

use Getopt::Long;
#use Statistics::Descriptive;

#parameter initialization
my $reference="tweetLID-training_ids.tsv";
my $data="";

my %params;

(GetOptions (\%params,
	    "data|d=s"=>\$data,
	    "reference|r=s"=>\$reference,
	    "help|h")) || die "ERROR: Illegal arguments or parameters: @ARGV\n" unless ($#ARGV < 0);


###########################
# Argument parsing
###########################

#usage
if (defined $params{"help"} || defined $params{"h"})
{
    die "$usage\n";
}
#if no data is given prints usage and exit
if ($data eq "")
{
    die "$usage\n No run file was specified\n";
}

warn "\nGold standard reference file: $reference \n";
warn "Provided run file: $data \n\n";

################################
#   End of argument parsing    #
################################



# hash to store the statistics used to compute P/R/F
my %stats;
my $success = &initializeStats(\%stats);

# Counters for answers
my $submitted = 0;
my $inRef = 0;
my $unanswered = 0;

# load reference
my %ref_hash;
my $refTweets=0;

open(REF, "< $reference") || die("Could not open reference file $reference .\n");
while($l=<REF>)
{    
    chomp $l;
    # lines starting with # are comments and are not considered. Blank lines are left out as well
    if (($l =~ /^#/) || ($l =~ /^\s*$/))
    {
	next;
    }

    (my $tweetid, my $userId, my $lang_ref, @other) = split /\s/, $l;    
    unless (defined $ref_hash{$tweetid})
    {
	$refTweets++;

	# other category is considered as und for evaluation purposes
	$lang_ref =~s/other/und/;
	# expand the correct answer alternatives lang1/lang2+lang3 => lang1+lang2::lang2+lang3 and lang1+lang2/lang3 => lang1+lang2::lang1+lang3
	my $tmplang = &expandCorrectAnswer($lang_ref); 
	
	$ref_hash{$tweetid} = $tmplang;
    }
    else
    {
	print STDERR "Warning: the tweet $tweetId was already in the reference, only the first annotation is taken into account\n";
    }
}
#reference loaded
close(REF);


my $Acc=0; 
#open run file
open(RUN, "< $data") || die("Could not open run file $data .\n");
while($l=<RUN>)
{   
    chomp $l;
    # lines starting with # are comments and are not considered. Blank lines are left out as well
    if (($l =~ /^#/) || ($l =~ /^\s*$/))
    {
	next;
    }
    
    (my $tweetid, my $langUser, @other) = split /\s/, $l;    

    $submitted++;

    # the tweet is not in the reference.
    if (!defined  $ref_hash{$tweetid})
    {
	print STDERR "Warning: the tweet $tweetId is not in the reference, won't be taken into account for computing the results.";	
	next;
    }
    
    $inRef++;

    # other category is considered as und for evaluation purposes
    $langUser =~ s/other/und/;


    # cleaning if the answer is lang1/lang2/lang3 take only lang1 as the provided answer
    if ($langUser =~/^([a-z]{2,5})(\/[a-z]{2,5})*$/)
    {
	my $langUser = $1;
    }
    
    # how much languages are needed in the answer
    (my $oneAlternative, @rest) = split /::/, $ref_hash{$tweetid};
    (my @requiredLangs) = split /\+/, $oneAlternative;
    my $requiredlangnum = scalar @requiredLangs;

    # cleaning if the answer is lang1+lang2+..+langn and n > 3
    (my @langsPlusRun) = split /\+/, $langUser;
    if (((scalar @langsPlusRun) > 3 ))
    {
	$langUser = join ('+',@langsPlusRun[0,2]);	
	$langUser =~ s/\+$//;
    }
 
    # First case: reference is a single language e.g. 'ca'
    if ($ref_hash{$tweetid} !~ /[\/\+]/)
    {
	my %found;
	my $fnum =0;
	my $correctLang= $ref_hash{$tweetid}."/";
	foreach my $ln (@langsPlusRun)
	{	    
	    if (($correctLang =~ /${ln}\//) && (!defined $found{$ln}))
	    {
		$stats{$ln}{"TP"}++;      
		$found{$ln}=1;
		$fnum++;
	    }
	    elsif (!defined $found{$ln})
	    {
		$stats{$ln}{"FP"}++;
	    }
	    else
	    {
		print STDERR "Warning: this shouldn't be hapenning - a language is repeated in the answer ... @langsPlusRun - #usr: $langUser vs. ref: $ref_hash{$tweetid}\n";
	    }
	}
	if ($fnum == 0)
	{
	    $stats{$ref_hash{$tweetid}}{"FN"}++;			    
	    #print STDERR "Warning: ref language not provided - #usr: $langUser vs. ref: $ref_hash{$tweetid}\n";
	}
    }    
    # Second case: multiple languages are correct. Reference is (lang1/lang2/...)
    elsif ( $ref_hash{$tweetid} =~ /\// )
    {
        my $correctLang= $ref_hash{$tweetid}."/";
	# single answer by the user
	if (scalar @langsPlusRun < 2)
	{
	    # usr lang1 - ref lang1/...
	    if ($correctLang =~ /${langUser}\//)
	    {
		$stats{"amb"}{"TP"}++;
	    }
	    # usr lang1 - ref lang2/lang3/...	    
	    else
	    {
		$stats{"$langUser"}{"FP"}++;
		$stats{"amb"}{"FN"}++;
	    }
	}
	#user answer is lang1+lang2+...
	else 
	{
	    # it is posible that the user has provided lang1+lang2 when the correct answer is lang1/lang2. In those cases:
	    # usr. lang1+lang2+lang4 vs. ref. lang1/lang2/lang3  -> amb TP, lang2 FP, lang4 FP
	    my $marked = 0;
	    foreach my $lng1 (@langsPlusRun)
	    {
                # ambiguous TP
		if (($correctLang =~ /${lng1}\//) && (! $marked))
		{
		    $stats{"amb"}{"TP"}++;
		    $marked=1;
		}
		# others FP (either wrong lang or a correct language already found)
		else
		{
		    $stats{$lng1}{"FP"}++;
		}
	    }
	    # No correct language among the answers -> ambiguous FN
	    if (!$marked)
	    {
		$stats{"amb"}{"FN"}++;
	    }
	}
    }
    # Third case: Multiple languages needed. Reference is lang1+lang2 or lang1+lang2::lang1+lang3::
    elsif ( $ref_hash{$tweetid} =~ /\+/)
    {	
	my %ocurred = {};
	my $TP = 0;
	# evaluate languages given in the run
	foreach my $lng (@langsPlusRun)
	{		
	    # Correct lang
	    if (($ref_hash{$tweetid} =~ /${lng}\+/) && (!defined $ocurred{$lng}))
	    {
		$stats{$lng}{"TP"}++;
		$ocurred{$lng}=1;
		$TP++;
	    }
	    #wrong lang
	    elsif  (!defined $ocurred{$lng})
	    {
		$stats{$lng}{"FP"}++;
	    }	
	}
	# langs not given in the answer should be counted as FN  
	# IMPORTANT! : es+gl/ca are not treated entirely, as only one of the two combinations is examined (either es+gl or es+ca)
	if ($TP < (scalar @requiredLangs))
	{
	    foreach my $ln (@requiredLangs)
	    {
		if  (!defined $ocurred{$ln})
		{
		    $stats{$ln}{"FN"}++;
		    #print STDERR "Warning: @langsPlusRun  - $langUser -  vs. ref: $ref_hash{$tweetid} - unekoa: $ln\n";	
		}
	    }
	}
    }
    # This conditions covers the FNs
    else
    {
	print STDERR "Warning: this case is not covered! => ref: $ref_hash{$tweetid} vs. @usr: $langUser\n";
    }

    # we don't need the tweet in the reference anymore. This will help us count those tweets in the reference that were not solved by the systems.
    delete $ref_hash{$tweetid};
}

close(RUN);

# compute P/R/F per category according to :
# Stefanie Nowak, Hanna Lukashevich, Peter Dunker, and Stefan Rüger. 2010. Performance measures for multilabel evaluation: a case study in the area of image classification. In Proceedings of the international conference on Multimedia information retrieval (MIR '10). ACM, New York, NY, USA, 35-44. DOI=10.1145/1743384.1743398 http://doi.acm.org/10.1145/1743384.1743398 

my $err = &computePRFperCategory(\%stats);

print "\n RESULTS ONLY taking into account SUBMITTED RESULTS IN THE REFERENCE: \n";    

my $err0 = &printResults(\%stats);

# Tweets that are in the reference but not in the run shall be counted for the computations of the recall
for my $tid (keys %{ref_hash})
{
    $unanswered++;
    #single language
    if ($ref_hash{$tid} !~ /[\/\+]/)
    {
	$stats{$ref_hash{$tid}}{"FN"}++;
    }
    # multiple languages allowed
    elsif ($ref_hash{$tid} =~ /\//)
    {
	$stats{"amb"}{"FN"}++;       
    }
    # multiple languages required
    elsif ($ref_hash{$tid} =~ /\+/)
    {
	(my $firstalter, my @others) = split /::/, $ref_hash{$tid};
	(my @langs) = split /\+/, $firstalter;
	foreach my $l (@langs)
	{
	    $stats{$l}{"FN"}++;
	}
    }
}

print "\nSubmitted run contains => $submitted tweets. From those $inRef are in the reference. \nProvided reference has => $refTweets tweets. From those $unanswered tweets were left unanswered. \n";

# compute P/R/F per category according to :
my $err1 = &computePRFperCategory(\%stats);

print "\n RESULTS taking into account ALL TWEETS in the reference (unanswered tweets affect Recall and Fscore negatively) \n";    

my $err2 = &printResults(\%stats);


#############################################################
#
#          Functions
#
#############################################################


sub expandCorrectAnswer()
{
    my $langIn = shift;

    # expand the correct answer alternatives lang1/lang2+lang3 => lang1+lang2::lang2+lang3 and lang1+lang2/lang3 => lang1+lang2::lang1+lang3
    my $tmplang = $langIn;
    $tmplang =~ s/^([a-z]{2,5})\/([a-z]{2,5})\+([a-z]{2,5})$/$1+$3::$2+$3::$3+$1::$3+$2::/;
    $tmplang =~ s/^([a-z]{2,5})\+([a-z]{2,5})\/([a-z]{2,5})$/$1+$2::$1+$3::$2+$1::$3+$1::/;
    
    # expand the correct answer alternatives lang1+lang2 => lang1+lang2::lang2+lang1 and lang1+lang2+lang3 => lang1+lang2+lang3::lang1+lang3+lang2::lang2+lang1+lang3::lang2+lang3+lang1::lang3+lang1+lang2::lang3+lang2+lang1::	
    unless ($tmplang =~ /\:\:/)
    {
	$tmplang =~ s/^([a-z]{2,5})\+([a-z]{2,5})$/$1+$2::$2+$1::/;
	$tmplang =~ s/^([a-z]{2,5})\+([a-z]{2,5})\+([a-z]{2,5})$/$1+$2+$3::$1+$3+$2::$2+$1+$3::$2+$3+$1::$3+$1+$2::$3+$2+$1::/;
    }
    
    return $tmplang;
}


sub initializeStats()
{
    my $hash_ref = shift;
    my @classes = ("es","en","eu","pt","gl","ca","amb","und");
    my @stats = ("TP","TN","FP","FN","P","R","F","N");
    
    foreach my $c (@classes)
    {
	foreach my $s (@stats)
	{
	    $hash_ref->{$c}{$s} = 0.0;
	}
    }

    return 0;
}

# compute P/R/F per category according to :
# Stefanie Nowak, Hanna Lukashevich, Peter Dunker, and Stefan Rüger. 2010. Performance measures for multilabel evaluation: a case study in the area of image classification. In Proceedings of the international conference on Multimedia information retrieval (MIR '10). ACM, New York, NY, USA, 35-44. DOI=10.1145/1743384.1743398 http://doi.acm.org/10.1145/1743384.1743398 
sub computePRFperCategory()
{
    my $hash_ref = shift;
    my $avgP = 0.0;
    my $avgR = 0.0;
    my $avgF = 0.0;
    my $C = 0;
    for my $cat (keys %{$hash_ref})
    {
	$C++;
	#print STDERR "$cat category stats computation : .. start ..  \n";
	if ( ($hash_ref->{$cat}{"TP"} + $hash_ref->{$cat}{"FP"}) > 0)
	{
	    $hash_ref->{$cat}{"P"} = 1.0*$hash_ref->{$cat}{"TP"} / ( $hash_ref->{$cat}{"TP"} + $hash_ref->{$cat}{"FP"} ) ;
	}	
	$avgP += $hash_ref->{$cat}{"P"};
	#print STDERR "$cat category stats computation : .. P .. $hash_ref->{$cat}{'P'} \n";
	if ( ($hash_ref->{$cat}{"TP"} + $hash_ref->{$cat}{"FN"}) > 0)
	{
	    $hash_ref->{$cat}{"R"} = 1.0*$hash_ref->{$cat}{"TP"} / ( $hash_ref->{$cat}{"TP"} + $hash_ref->{$cat}{"FN"} ) ;
	}
	$avgR += $hash_ref->{$cat}{"R"};
	#print STDERR "$cat category stats computation : .. R .. $hash_ref->{$cat}{'R'} \n";
	if ( ($hash_ref->{$cat}{"TP"} + $hash_ref->{$cat}{"FN"} + $hash_ref->{$cat}{"FP"}) > 0)
	{
	    $hash_ref->{$cat}{"F"} = ( 2*$hash_ref->{$cat}{"TP"} / ( 2.0*$hash_ref->{$cat}{"TP"} + $hash_ref->{$cat}{"FN"} + $hash_ref->{$cat}{"FP"} ) );	
	}
	$avgF += $hash_ref->{$cat}{"F"};
	#print STDERR "$cat category stats computation : .. F ..  $hash_ref->{$cat}{'F'} \n";
    }
    

    $hash_ref->{"Global"}{"P"} = $avgP/$C;
    $hash_ref->{"Global"}{"R"} = $avgR/$C;
    $hash_ref->{"Global"}{"F"} = $avgF/$C;
    

    return 0;
}

sub printResults()
{
    my $hash_ref = shift;
    
    for my $cat (keys %{$hash_ref})
    {
	unless ($cat eq "Global")
	{
	    print "Category $cat : P => $hash_ref->{$cat}{P} , R => $hash_ref->{$cat}{R} , F => $hash_ref->{$cat}{F} \n";    
	}
    }
    
    print "\nGlobal results : P => $hash_ref->{'Global'}{P} , R => $hash_ref->{'Global'}{R} , F => $hash_ref->{'Global'}{F} \n";    
    
    return 0;
}
